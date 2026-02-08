import json
from asgiref.sync import sync_to_async

from . import ai_engine


class HealthForecaster:
    """Adapter that delegates data collection and AI calls to `dashboard.ai_engine`.

    Provides both synchronous and async entrypoints while reusing the same
    service functions in `ai_engine.py` to keep behavior consistent.
    """

    def __init__(self, user):
        self.user = user

    # Sync wrappers delegate to ai_engine
    def collect_health_data(self):
        return ai_engine.collect_health_data(self.user)

    def ai_recommendations(self, data):
        return ai_engine.call_ai(data)

    def store_result(self, ai_data):
        return ai_engine.store_ai_result(self.user, ai_data)

    def get_forecast_data(self):
        data = self.collect_health_data()
        ai_result = self.ai_recommendations(data)
        try:
            self.store_result(ai_result)
        except Exception:
            # Non-fatal: don't break request flow if storage fails
            pass

        return {
            "health_score": ai_result.get("health_score", 60),
            "risks": ai_result.get("risks", {}),
            "recommendations": ai_result.get("recommendations", []),
            "priority_actions": ai_result.get("priority_actions", []),
            "warnings": ai_result.get("warnings", []),
            "raw_ai": ai_result,
        }

    # Async wrappers
    async def collect_health_data_async(self):
        return await sync_to_async(ai_engine.collect_health_data)(self.user)

    async def ai_recommendations_async(self, data):
        return await sync_to_async(ai_engine.call_ai)(data)

    async def store_result_async(self, ai_data):
        return await sync_to_async(ai_engine.store_ai_result)(self.user, ai_data)

    async def get_forecast_data_async(self):
        data = await self.collect_health_data_async()
        ai_result = await self.ai_recommendations_async(data)
        try:
            await self.store_result_async(ai_result)
        except Exception:
            pass

        return {
            "health_score": ai_result.get("health_score", 60),
            "risks": ai_result.get("risks", {}),
            "recommendations": ai_result.get("recommendations", []),
            "priority_actions": ai_result.get("priority_actions", []),
            "warnings": ai_result.get("warnings", []),
            "raw_ai": ai_result,
        }
