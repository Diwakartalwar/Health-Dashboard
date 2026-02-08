import threading
import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache

from . import ai_engine

logger = logging.getLogger(__name__)

User = get_user_model()


def _run_ai_for_user(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("User %s does not exist for AI run", user_id)
        return

    try:
        data = ai_engine.collect_health_data(user)
        ai_result = ai_engine.call_ai(data)
        ai_engine.store_ai_result(user, ai_result)
        logger.info("AI forecast completed for user %s", user_id)
    except Exception:
        logger.exception("Failed to run AI forecast for user %s", user_id)


def enqueue_ai_forecast(user_id):
    """Enqueue AI forecast work.

    Default dev fallback uses a background thread. Replace or extend
    with Celery/Django-Q integration in production.
    """
    t = threading.Thread(target=_run_ai_for_user, args=(user_id,), daemon=True)
    t.start()
    return t
