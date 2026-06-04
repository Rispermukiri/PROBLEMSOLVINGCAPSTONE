"""
Students app URL configuration.
Handles student profile endpoints.
"""

from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('profile/', views.StudentProfileView.as_view(), name='profile'),
    path('profile/<int:student_id>/', views.StudentProfileDetailView.as_view(), name='profile-detail'),
]
