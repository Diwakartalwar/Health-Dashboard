from django.contrib import admin
from .models import BloodReport, VitalSigns, HealthMetric


@admin.register(BloodReport)
class BloodReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'glucose_mg_dl', 'total_cholesterol_mg_dl')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'date'


@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'systolic_bp', 'diastolic_bp', 'heart_rate_bpm')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'date'


@admin.register(HealthMetric)
class HealthMetricAdmin(admin.ModelAdmin):
    list_display = ('user', 'metric_type', 'value', 'date')
    list_filter = ('metric_type', 'date', 'user')
    search_fields = ('user__username',)
    date_hierarchy = 'date'
