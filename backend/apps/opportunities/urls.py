"""
Opportunities app URL configuration.
Handles job posting endpoints.
"""

from django.urls import path
from . import views

app_name = 'opportunities'

urlpatterns = [
    path('', views.OpportunityListView.as_view(), name='list'),
    path('create/', views.CreateOpportunityView.as_view(), name='create'),
    path('<int:opportunity_id>/', views.OpportunityDetailView.as_view(), name='detail'),
    path('<int:opportunity_id>/update/', views.UpdateOpportunityView.as_view(), name='update'),
    path('<int:opportunity_id>/delete/', views.DeleteOpportunityView.as_view(), name='delete'),
]
