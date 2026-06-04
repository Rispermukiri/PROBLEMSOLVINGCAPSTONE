"""
Applications app URL configuration.
Handles student application endpoints.
"""

from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.ApplicationsListView.as_view(), name='list'),
    path('apply/', views.ApplyView.as_view(), name='apply'),
    path('<int:application_id>/', views.ApplicationDetailView.as_view(), name='detail'),
    path('<int:application_id>/withdraw/', views.WithdrawApplicationView.as_view(), name='withdraw'),
]
