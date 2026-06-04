"""
Opportunity views for AttachLink.
Handles internship posting CRUD operations, listing, and filtering.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.employers.models import Employer
from apps.opportunities.models import Opportunity
from apps.opportunities.permissions import IsOpportunityOwner
from apps.opportunities.serializers import (
    OpportunityCreateUpdateSerializer,
    OpportunityDetailSerializer,
    OpportunityListSerializer,
)
from apps.opportunities.services import OpportunityService
from utils.permissions import IsEmployer, IsVerifiedEmployer


class OpportunityListView(generics.ListAPIView):
    """List active opportunities for students and visitors."""
    serializer_class = OpportunityListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = OpportunityService.get_public_queryset()
        return OpportunityService.filter_queryset(queryset, self.request.query_params)

    @extend_schema(
        operation_id='list_opportunities',
        description='List open internship and attachment opportunities.',
        responses=OpportunityListSerializer,
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created_at')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        start = (page - 1) * page_size
        end = start + page_size
        paged = queryset[start:end]

        return Response({
            'count': queryset.count(),
            'page': page,
            'page_size': page_size,
            'results': self.get_serializer(paged, many=True).data,
        }, status=status.HTTP_200_OK)


class CreateOpportunityView(generics.CreateAPIView):
    """Create a new internship opportunity (employers only)."""
    serializer_class = OpportunityCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer, IsVerifiedEmployer]

    @extend_schema(
        operation_id='create_opportunity',
        description='Create a new opportunity for the authenticated employer.',
        request=OpportunityCreateUpdateSerializer,
        responses=OpportunityDetailSerializer,
    )
    def create(self, request, *args, **kwargs):
        try:
            employer = Employer.objects.get(user=request.user)
        except Employer.DoesNotExist:
            return Response(
                {'detail': 'Employer profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        opportunity = OpportunityService.create_opportunity(employer, serializer.validated_data)
        output = OpportunityDetailSerializer(opportunity)
        return Response(output.data, status=status.HTTP_201_CREATED)


class OpportunityDetailView(generics.RetrieveAPIView):
    """Retrieve opportunity detail for students and visitors."""
    queryset = Opportunity.objects.filter(is_deleted=False).select_related('employer')
    serializer_class = OpportunityDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'
    lookup_url_kwarg = 'opportunity_id'

    @extend_schema(
        operation_id='retrieve_opportunity',
        description='Retrieve a specific opportunity by ID.',
        responses=OpportunityDetailSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        opportunity = self.get_object()
        OpportunityService.increment_view_count(opportunity)
        serializer = self.get_serializer(opportunity)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateOpportunityView(generics.UpdateAPIView):
    """Update an existing opportunity (owning employer only)."""
    queryset = Opportunity.objects.filter(is_deleted=False)
    serializer_class = OpportunityCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer, IsOpportunityOwner]
    lookup_field = 'id'
    lookup_url_kwarg = 'opportunity_id'

    @extend_schema(
        operation_id='update_opportunity',
        description='Update an employer-owned opportunity.',
        request=OpportunityCreateUpdateSerializer,
        responses=OpportunityDetailSerializer,
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        opportunity = OpportunityService.update_opportunity(instance, serializer.validated_data)
        output = OpportunityDetailSerializer(opportunity)
        return Response(output.data, status=status.HTTP_200_OK)


class DeleteOpportunityView(generics.DestroyAPIView):
    """Soft delete an opportunity (owning employer only)."""
    queryset = Opportunity.objects.filter(is_deleted=False)
    permission_classes = [permissions.IsAuthenticated, IsEmployer, IsOpportunityOwner]
    lookup_field = 'id'
    lookup_url_kwarg = 'opportunity_id'

    @extend_schema(
        operation_id='delete_opportunity',
        description='Soft delete an employer-owned opportunity.',
        responses={204: None},
    )
    def perform_destroy(self, instance):
        OpportunityService.soft_delete_opportunity(instance)
