from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Avg, Count
from datetime import datetime, timedelta
import json
import csv
from health_metrics.models import BloodReport, VitalSigns, HealthMetric
from health_metrics.forms import HealthMetricForm
from .models import HealthForecast, AIForecast
from django.core.cache import cache

@login_required
def dashboard_overview(request):
    user = request.user

    # ----------------------------
    # Load AI data (cache → DB)
    # ----------------------------
    cache_key = f"ai_forecast_{user.id}"
    ai_data = cache.get(cache_key)

    if ai_data is None:
        try:
            ai_obj = AIForecast.objects.get(user=user)
            ai_data = ai_obj.ai_data
            cache.set(cache_key, ai_data, timeout=3600)
        except AIForecast.DoesNotExist:
            ai_data = None

    # ----------------------------
    # HealthForecast (rule storage)
    # ----------------------------
    health_forecast, _ = HealthForecast.objects.get_or_create(user=user)

    if ai_data:
        # Fix health_score if None
        health_score = ai_data.get("health_score")
        if health_score is None:
            health_score = 60  # Default score
        
        health_forecast.health_score = health_score

        risks = ai_data.get("risks", {})
        health_forecast.cardiovascular_risk = risks.get(
            "cardiovascular", health_forecast.cardiovascular_risk
        )
        health_forecast.diabetes_risk = risks.get(
            "diabetes", health_forecast.diabetes_risk
        )

        health_forecast.save()

    # ----------------------------
    # Metrics
    # ----------------------------
    latest_blood = (
        BloodReport.objects.filter(user=user).latest("date")
        if BloodReport.objects.filter(user=user).exists()
        else None
    )

    latest_vitals = (
        VitalSigns.objects.filter(user=user)
        .order_by("-date", "-time")
        .first()
    )

    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    blood_reports = BloodReport.objects.filter(
        user=user, date__gte=thirty_days_ago
    ).order_by("date")

    vital_signs = VitalSigns.objects.filter(
        user=user, date__gte=thirty_days_ago
    ).order_by("date")

    # ----------------------------
    # FRONTEND-SAFE CONTEXT
    # ----------------------------
    context = {
        "forecast": health_forecast,
        "latest_blood": latest_blood,
        "latest_vitals": latest_vitals,
        "blood_reports": blood_reports,
        "vital_signs": vital_signs,

        # 👇 THIS IS THE FIX
        "recommendations": (
            ai_data.get("recommendations", [])
            if ai_data
            else []
        ),

        "ai_ready": bool(ai_data),
    }

    return render(request, "dashboard/overview.html", context)


@login_required
def dashboard_overview_debug(request):
    """Debug version of dashboard overview"""
    user = request.user

    # ----------------------------
    # Load AI data (cache → DB)
    # ----------------------------
    cache_key = f"ai_forecast_{user.id}"
    ai_data = cache.get(cache_key)

    if ai_data is None:
        try:
            ai_obj = AIForecast.objects.get(user=user)
            ai_data = ai_obj.ai_data
            cache.set(cache_key, ai_data, timeout=3600)
        except AIForecast.DoesNotExist:
            ai_data = None

    # ----------------------------
    # HealthForecast (rule storage)
    # ----------------------------
    health_forecast, _ = HealthForecast.objects.get_or_create(user=user)

    if ai_data:
        # Fix health_score if None
        health_score = ai_data.get("health_score")
        if health_score is None:
            health_score = 60  # Default score
        
        health_forecast.health_score = health_score

        risks = ai_data.get("risks", {})
        health_forecast.cardiovascular_risk = risks.get(
            "cardiovascular", health_forecast.cardiovascular_risk
        )
        health_forecast.diabetes_risk = risks.get(
            "diabetes", health_forecast.diabetes_risk
        )

        health_forecast.save()

    # ----------------------------
    # FRONTEND-SAFE CONTEXT
    # ----------------------------
    context = {
        "forecast": health_forecast,
        "recommendations": (
            ai_data.get("recommendations", [])
            if ai_data
            else []
        ),
        "ai_ready": bool(ai_data),
    }

    return render(request, "dashboard/overview_debug.html", context)



@login_required
def blood_trend(request):
    """Blood metrics trend chart data"""
    user = request.user
    thirty_days_ago = datetime.now().date() - timedelta(days=30)
    
    blood_reports = BloodReport.objects.filter(
        user=user,
        date__gte=thirty_days_ago
    ).order_by('date')
    
    data = {
        'dates': [],
        'glucose': [],
        'total_cholesterol': [],
        'ldl': [],
        'hdl': [],
    }
    
    for report in blood_reports:
        data['dates'].append(str(report.date))
        data['glucose'].append(report.glucose_mg_dl)
        data['total_cholesterol'].append(report.total_cholesterol_mg_dl)
        data['ldl'].append(report.ldl_cholesterol_mg_dl)
        data['hdl'].append(report.hdl_cholesterol_mg_dl)
    
    return JsonResponse(data)


@login_required
def vital_trend(request):
    """Vital signs trend chart data"""
    user = request.user
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    
    vital_signs = VitalSigns.objects.filter(
        user=user,
        date__gte=seven_days_ago
    ).order_by('date', 'time')
    
    data = {
        'dates': [],
        'systolic': [],
        'diastolic': [],
        'heart_rate': [],
    }
    
    for vital in vital_signs:
        data['dates'].append(f"{vital.date} {vital.time}")
        data['systolic'].append(vital.systolic_bp)
        data['diastolic'].append(vital.diastolic_bp)
        data['heart_rate'].append(vital.heart_rate_bpm)
    
    return JsonResponse(data)


@login_required
def health_metrics_trend(request):
    """Health metrics trend data"""
    user = request.user
    metric_type = request.GET.get('metric_type', 'weight')
    
    seven_days_ago = datetime.now().date() - timedelta(days=7)
    
    metrics = HealthMetric.objects.filter(
        user=user,
        metric_type=metric_type,
        date__gte=seven_days_ago
    ).order_by('date')
    
    data = {
        'dates': [str(m.date) for m in metrics],
        'values': [m.value for m in metrics],
    }
    
    return JsonResponse(data)


@login_required
def analytics_dashboard(request):
    """Enhanced analytics dashboard with interactive charts"""
    user = request.user
    
    # Get recent health metrics for goal tracking
    recent_metrics = HealthMetric.objects.filter(user=user).order_by('-date')[:30]
    
    # Calculate goal progress
    goals_with_progress = []
    for metric_type in ['weight', 'exercise', 'sleep']:
        metrics = HealthMetric.objects.filter(user=user, metric_type=metric_type).order_by('-date')[:7]
        if metrics:
            latest = metrics.first()
            # Check if goal exists
            if hasattr(latest, 'target_value'):
                progress = (latest.value / latest.target_value) * 100 if latest.target_value else 0
                goals_with_progress.append({
                    'name': metric_type.replace('_', ' ').title(),
                    'current_value': latest.value,
                    'target_value': latest.target_value,
                    'progress': min(progress, 100)
                })
    
    context = {
        'user': user,
        'goals': goals_with_progress,
        'recent_metrics': recent_metrics
    }
    
    return render(request, 'dashboard/analytics.html', context)


@login_required
def export_health_data(request):
    """Export health data as CSV"""
    user = request.user
    export_type = request.GET.get('type', 'all')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="health_data_{export_type}_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    writer = csv.writer(response)
    
    if export_type == 'blood':
        writer.writerow(['Date', 'Glucose', 'Total Cholesterol', 'LDL', 'HDL', 'Triglycerides', 'Hemoglobin', 'Creatinine', 'BUN'])
        blood_reports = BloodReport.objects.filter(user=user).order_by('-date')
        for report in blood_reports:
            writer.writerow([
                report.date,
                report.glucose_mg_dl,
                report.total_cholesterol_mg_dl,
                report.ldl_cholesterol_mg_dl,
                report.hdl_cholesterol_mg_dl,
                report.triglycerides_mg_dl,
                report.hemoglobin_g_dl,
                report.creatinine_mg_dl,
                report.bun_mg_dl
            ])
    
    elif export_type == 'vitals':
        writer.writerow(['Date', 'Time', 'Systolic BP', 'Diastolic BP', 'Heart Rate', 'Temperature', 'Oxygen Saturation'])
        vitals = VitalSigns.objects.filter(user=user).order_by('-date', '-time')
        for vital in vitals:
            writer.writerow([
                vital.date,
                vital.time,
                vital.systolic_bp,
                vital.diastolic_bp,
                vital.heart_rate_bpm,
                vital.temperature_celsius,
                vital.oxygen_saturation
            ])
    
    else:  # all
        writer.writerow(['Type', 'Date', 'Metric', 'Value', 'Notes'])
        
        # Blood reports
        blood_reports = BloodReport.objects.filter(user=user).order_by('-date')
        for report in blood_reports:
            if report.glucose_mg_dl:
                writer.writerow(['Blood', report.date, 'Glucose', report.glucose_mg_dl, ''])
            if report.total_cholesterol_mg_dl:
                writer.writerow(['Blood', report.date, 'Total Cholesterol', report.total_cholesterol_mg_dl, ''])
        
        # Vital signs
        vitals = VitalSigns.objects.filter(user=user).order_by('-date', '-time')
        for vital in vitals:
            if vital.systolic_bp:
                writer.writerow(['Vitals', f"{vital.date} {vital.time}", 'Systolic BP', vital.systolic_bp, ''])
            if vital.heart_rate_bpm:
                writer.writerow(['Vitals', f"{vital.date} {vital.time}", 'Heart Rate', vital.heart_rate_bpm, ''])
        
        # Health metrics
        metrics = HealthMetric.objects.filter(user=user).order_by('-date')
        for metric in metrics:
            writer.writerow(['Metric', metric.date, metric.get_metric_type_display(), metric.value, metric.notes])
    
    return response


@login_required
def goals_api(request):
    """API endpoint for goal progress data"""
    user = request.user
    goals = []
    
    for metric_type in ['weight', 'exercise', 'sleep']:
        metrics = HealthMetric.objects.filter(user=user, metric_type=metric_type).order_by('-date')[:7]
        if metrics:
            latest = metrics.first()
            if hasattr(latest, 'target_value'):
                goals.append({
                    'name': metric_type.replace('_', ' ').title(),
                    'current_value': latest.value,
                    'target_value': latest.target_value,
                    'progress': min((latest.value / latest.target_value) * 100 if latest.target_value else 0, 100)
                })
    
    return JsonResponse({'goals': goals})


@login_required
def goals_dashboard(request):
    """Goals and progress tracking dashboard"""
    user = request.user
    
    # Get metrics with goals
    metrics_with_goals = HealthMetric.objects.filter(
        user=user,
        target_value__isnull=False
    ).order_by('-date')
    
    # Get recent metrics for table
    recent_metrics = HealthMetric.objects.filter(user=user).order_by('-date')[:20]
    
    context = {
        'goals': metrics_with_goals,
        'recent_metrics': recent_metrics,
        'form': HealthMetricForm()
    }
    
    return render(request, 'dashboard/goals.html', context)
