"""
Main URL configuration for AttachLink project.
Routes for all apps and API endpoints.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# API versioning and namespacing
API_PREFIX = 'api/v1/'

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls, name='admin'),

    # API Documentation
    path(f'{API_PREFIX}schema/', SpectacularAPIView.as_view(), name='schema'),
    path(f'{API_PREFIX}docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path(f'{API_PREFIX}redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # App URLs
    path(f'{API_PREFIX}auth/', include('apps.users.urls', namespace='auth')),
    path(f'{API_PREFIX}students/', include('apps.students.urls', namespace='students')),
    path(f'{API_PREFIX}employers/', include('apps.employers.urls', namespace='employers')),
    path(f'{API_PREFIX}opportunities/', include('apps.opportunities.urls', namespace='opportunities')),
    path(f'{API_PREFIX}applications/', include('apps.applications.urls', namespace='applications')),
    path(f'{API_PREFIX}admin/', include('apps.admin_panel.urls', namespace='admin_panel')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Admin Customization
admin.site.site_header = 'AttachLink Administration'
admin.site.site_title = 'AttachLink Admin'
admin.site.index_title = 'Welcome to AttachLink Administration'
