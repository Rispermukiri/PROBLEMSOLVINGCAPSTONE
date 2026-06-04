"""
Admin Panel app URL configuration.
Handles admin dashboard and moderation endpoints.
"""

from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('flagged-content/', views.FlaggedContentListView.as_view(), name='flagged-content'),
    path('flagged-content/<int:flag_id>/resolve/', views.ResolveFlagView.as_view(), name='resolve-flag'),
]
