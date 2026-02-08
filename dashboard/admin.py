from django.contrib import admin
from .models import HealthForecast


@admin.register(HealthForecast)
class HealthForecastAdmin(admin.ModelAdmin):
    list_display = ('user', 'health_score', 'cardiovascular_risk', 'diabetes_risk', 'generated_at')
    list_filter = ('cardiovascular_risk', 'diabetes_risk', 'generated_at')
    search_fields = ('user__username',)
    readonly_fields = ('generated_at',)
