from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'health_metrics'

router = DefaultRouter()
router.register(r'blood-reports', views.BloodReportViewSet, basename='blood-report')
router.register(r'vital-signs', views.VitalSignsViewSet, basename='vital-signs')
router.register(r'health-metrics', views.HealthMetricViewSet, basename='health-metric')

urlpatterns = [
    # API endpoints live under /metrics/api/ to avoid colliding with web views
    path('api/', include(router.urls)),
    
    # Web views
    path('blood-reports/', views.blood_report_list, name='blood_report_list'),
    path('blood-reports/add/', views.add_blood_report, name='add_blood_report'),
    path('blood-reports/<int:pk>/edit/', views.edit_blood_report, name='edit_blood_report'),
    path('blood-reports/<int:pk>/delete/', views.delete_blood_report, name='delete_blood_report'),
    
    path('vital-signs/', views.vital_signs_list, name='vital_signs_list'),
    path('vital-signs/add/', views.add_vital_signs, name='add_vital_signs'),
    
    path('health-metrics/', views.health_metric_list, name='health_metric_list'),
    path('health-metrics/add/', views.add_health_metric, name='add_health_metric'),
]
