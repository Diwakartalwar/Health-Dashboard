from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class HealthForecast(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_forecast')
    generated_at = models.DateTimeField(auto_now=True)
    
    # Overall health score 0-100
    health_score = models.FloatField(default=50)
    
    # Risk levels
    cardiovascular_risk = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')],
        default='moderate'
    )
    diabetes_risk = models.CharField(
        max_length=20,
        choices=[('low', 'Low'), ('moderate', 'Moderate'), ('high', 'High')],
        default='moderate'
    )
    
    # Recommendations
    recommendations = models.JSONField(default=list)
    
    def __str__(self):
        return f"Health Forecast for {self.user.username}"


class AIForecast(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ai_forecast')
    ai_data = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Forecast for {self.user.username} (updated {self.updated_at.isoformat()})"
