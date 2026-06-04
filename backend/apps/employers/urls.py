"""
Employers app URL configuration.
Handles employer profile endpoints.
"""

from django.urls import path
from . import views

app_name = 'employers'

urlpatterns = [
    path('profile/', views.EmployerProfileView.as_view(), name='profile'),
    path('profile/<int:employer_id>/', views.EmployerProfileDetailView.as_view(), name='profile-detail'),
]
