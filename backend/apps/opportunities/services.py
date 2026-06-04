from django.db.models import Q

from apps.employers.models import Employer
from apps.opportunities.models import Opportunity


class OpportunityService:
    """Encapsulates opportunity business logic and query composition."""

    @staticmethod
    def get_public_queryset():
        return Opportunity.objects.filter(
            is_deleted=False,
            status='open'
        ).select_related('employer')

    @staticmethod
    def get_queryset():
        return Opportunity.objects.filter(is_deleted=False).select_related('employer')

    @staticmethod
    def filter_queryset(queryset, params):
        employment_type = params.get('employment_type')
        location = params.get('location')
        is_remote = params.get('is_remote')
        is_featured = params.get('is_featured')
        search = params.get('search')

        if employment_type:
            queryset = queryset.filter(employment_type=employment_type)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if is_remote is not None:
            if isinstance(is_remote, str):
                is_remote = is_remote.lower() == 'true'
            queryset = queryset.filter(is_remote=is_remote)
        if is_featured is not None:
            if isinstance(is_featured, str):
                is_featured = is_featured.lower() == 'true'
            queryset = queryset.filter(is_featured=is_featured)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(requirements__icontains=search) |
                Q(employer__company_name__icontains=search)
            )

        return queryset

    @staticmethod
    def get_opportunity(opportunity_id):
        return Opportunity.objects.select_related('employer').get(id=opportunity_id, is_deleted=False)

    @staticmethod
    def create_opportunity(employer: Employer, validated_data):
        opportunity = Opportunity.objects.create(employer=employer, **validated_data)
        employer.increment_postings()
        return opportunity

    @staticmethod
    def update_opportunity(opportunity: Opportunity, validated_data):
        for attr, value in validated_data.items():
            setattr(opportunity, attr, value)
        opportunity.save()
        return opportunity

    @staticmethod
    def soft_delete_opportunity(opportunity: Opportunity):
        opportunity.soft_delete()
        return opportunity

    @staticmethod
    def increment_view_count(opportunity: Opportunity):
        opportunity.update_view_count()
        return opportunity
