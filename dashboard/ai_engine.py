import json
import logging
import re
from datetime import datetime, timedelta

import requests
from django.conf import settings
from django.core.cache import cache
from django.db.models import Avg, Sum

from .models import AIForecast
from health_metrics.models import BloodReport, VitalSigns, HealthMetric
from accounts.models import UserProfile

logger = logging.getLogger(__name__)

# =========================
# OLLAMA CONFIG
# =========================
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "lexillama"   # must match `ollama run lexillama`


# =========================
# DATA COLLECTION
# =========================
def collect_health_data(user):
    """Collect latest and aggregated health data for a user."""
    data = {}

    # ---- Blood Report ----
    try:
        blood = BloodReport.objects.filter(user=user).latest("date")
        data["blood_report"] = {
            "glucose": blood.glucose_mg_dl,
            "total_cholesterol": blood.total_cholesterol_mg_dl,
            "hdl": blood.hdl_cholesterol_mg_dl,
            "ldl": blood.ldl_cholesterol_mg_dl,
            "hemoglobin": blood.hemoglobin_g_dl,
            "creatinine": blood.creatinine_mg_dl,
            "bun": blood.bun_mg_dl,
        }
    except Exception:
        data["blood_report"] = {}

    # ---- Vitals ----
    try:
        vitals = (
            VitalSigns.objects
            .filter(user=user)
            .order_by("-date", "-time")
            .first()
        )
        data["vitals"] = {
            "systolic_bp": vitals.systolic_bp,
            "diastolic_bp": vitals.diastolic_bp,
            "heart_rate": vitals.heart_rate_bpm,
            "oxygen": vitals.oxygen_saturation,
            "temperature": vitals.temperature_celsius,
        }
    except Exception:
        data["vitals"] = {}

    # ---- Lifestyle (last 7 days) ----
    seven_days_ago = datetime.now().date() - timedelta(days=7)

    def avg_metric(metric_type):
        qs = HealthMetric.objects.filter(
            user=user,
            metric_type=metric_type,
            date__gte=seven_days_ago,
        )
        return qs.aggregate(Avg("value"))["value__avg"] if qs.exists() else None

    try:
        sleep_avg = avg_metric("sleep")
    except Exception:
        sleep_avg = None

    try:
        stress_avg = avg_metric("stress")
    except Exception:
        stress_avg = None

    try:
        exercise_total = (
            HealthMetric.objects
            .filter(user=user, metric_type="exercise", date__gte=seven_days_ago)
            .aggregate(Sum("value"))["value__sum"] or 0
        )
    except Exception:
        exercise_total = 0

    data["lifestyle"] = {
        "sleep_avg": sleep_avg,
        "stress_avg": stress_avg,
        "exercise_total": exercise_total,
    }

    # ---- Profile ----
    try:
        profile = UserProfile.objects.get(user=user)
        data["profile"] = {
            "age": profile.age,
            "gender": profile.gender,
            "bmi": profile.bmi,
            "height": profile.height,
            "weight": profile.weight,
        }
    except Exception:
        data["profile"] = {}

    return data


# =========================
# PROMPT
# =========================
def _build_prompt(data):
    return f"""
You are a medical explanation assistant.

RULES:
- You do NOT diagnose.
- You do NOT change risk levels.
- You do NOT invent numbers.
- You return ONLY valid JSON.
- NO markdown.
- NO text outside JSON.

RETURN JSON IN THIS EXACT FORMAT:
{{
  "health_score": null,
  "risks": {{
    "kidney": "low|moderate|high",
    "diabetes": "low|moderate|high",
    "cardiovascular": "low|moderate|high",
    "anemia": "low|moderate|high",
    "obesity": "low|moderate|high"
  }},
  "recommendations": [],
  "priority_actions": [],
  "warnings": []
}}

HEALTH DATA:
{json.dumps(data, indent=2)}
"""


# =========================
# AI CALL (OLLAMA)
# =========================
def _extract_json(text):
    # First try to find JSON in markdown code blocks
    # Pattern for ```json...``` or ```...```
    code_block_match = re.search(r'```(?:json)?\s*\n?(.*?)\n?```', text, re.S | re.I)
    if code_block_match:
        json_text = code_block_match.group(1).strip()
    else:
        # Fallback to original method - find JSON object in text
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise ValueError("No JSON found in AI output")
        json_text = match.group()
    
    try:
        json_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        # If parsing fails, try to clean up common issues
        # Remove trailing commas, fix quotes, etc.
        cleaned = json_text.replace(',\n}', '\n}').replace(',\n]', '\n]')
        json_data = json.loads(cleaned)
    
    # Fix recommendations format - ensure they're strings
    if 'recommendations' in json_data:
        recommendations = json_data['recommendations']
        if recommendations and isinstance(recommendations[0], dict):
            json_data['recommendations'] = [rec.get('text', str(rec)) for rec in recommendations]
    
    # Fix priority_actions format
    if 'priority_actions' in json_data:
        priority_actions = json_data['priority_actions']
        if priority_actions and isinstance(priority_actions[0], dict):
            json_data['priority_actions'] = [action.get('text', str(action)) for action in priority_actions]
    
    # Fix warnings format
    if 'warnings' in json_data:
        warnings = json_data['warnings']
        if warnings and isinstance(warnings[0], dict):
            json_data['warnings'] = [warning.get('text', str(warning)) for warning in warnings]
    
    return json_data


def call_ai(data, timeout=120):
    """
    Call local Ollama (LexiLLaMA).
    """
    prompt = _build_prompt(data)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_ctx": 4096,
                },
            },
            timeout=timeout,
        )
        response.raise_for_status()

        raw_text = response.json().get("response", "")
        return _extract_json(raw_text)

    except Exception:
        logger.exception("Ollama AI failed; using fallback")
        return {
            "health_score": 60,
            "risks": {},
            "recommendations": ["AI unavailable"],
            "priority_actions": [],
            "warnings": ["ai_error"],
        }


# =========================
# STORE RESULT
# =========================
def store_ai_result(user, ai_data):
    """Save AI result and cache it."""
    if user is None:
        return None

    obj, _ = AIForecast.objects.update_or_create(
        user=user,
        defaults={"ai_data": ai_data},
    )

    cache_key = f"ai_forecast_{user.id}"
    try:
        cache.set(cache_key, ai_data, timeout=3600)
    except Exception:
        logger.exception("Failed to cache AI result")

    return obj
