"""
URL configuration for health_forecast project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='accounts:register', permanent=False)),
    path('admin/', admin.site.urls),
    # Include custom apps under prefixed namespaces so templates can use namespaced reverses
    path('accounts/', include(("accounts.urls", "accounts"), namespace='accounts')),
    path('metrics/', include(("health_metrics.urls", "health_metrics"), namespace='health_metrics')),
    path('dashboard/', include(("dashboard.urls", "dashboard"), namespace='dashboard')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
