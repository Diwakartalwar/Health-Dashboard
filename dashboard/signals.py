import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

from health_metrics.models import BloodReport, VitalSigns, HealthMetric
from accounts.models import UserProfile

from .tasks import enqueue_ai_forecast

logger = logging.getLogger(__name__)


@receiver(post_save, sender=BloodReport)
def bloodreport_saved(sender, instance, created, **kwargs):
    try:
        user = instance.user
        enqueue_ai_forecast(user.id)
    except Exception:
        logger.exception("Failed to enqueue AI forecast on BloodReport save for %s", getattr(instance, 'id', None))


@receiver(post_save, sender=VitalSigns)
def vitals_saved(sender, instance, created, **kwargs):
    try:
        user = instance.user
        enqueue_ai_forecast(user.id)
    except Exception:
        logger.exception("Failed to enqueue AI forecast on VitalSigns save for %s", getattr(instance, 'id', None))


@receiver(post_save, sender=HealthMetric)
def healthmetric_saved(sender, instance, created, **kwargs):
    try:
        user = instance.user
        enqueue_ai_forecast(user.id)
    except Exception:
        logger.exception("Failed to enqueue AI forecast on HealthMetric save for %s", getattr(instance, 'id', None))


@receiver(post_save, sender=UserProfile)
def userprofile_saved(sender, instance, created, **kwargs):
    try:
        user = instance.user
        enqueue_ai_forecast(user.id)
    except Exception:
        logger.exception("Failed to enqueue AI forecast on UserProfile save for %s", getattr(instance, 'user', None))
