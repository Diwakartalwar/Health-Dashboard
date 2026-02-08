from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('overview/', views.dashboard_overview, name='overview'),
    path('overview/debug/', views.dashboard_overview_debug, name='overview_debug'),
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('goals/', views.goals_dashboard, name='goals'),
    path('api/export/', views.export_health_data, name='export_data'),
    path('api/goals/', views.goals_api, name='goals_api'),
    path('api/blood-trend/', views.blood_trend, name='blood_trend'),
    path('api/vital-trend/', views.vital_trend, name='vital_trend'),
    path('api/health-metrics-trend/', views.health_metrics_trend, name='health_metrics_trend'),
]
