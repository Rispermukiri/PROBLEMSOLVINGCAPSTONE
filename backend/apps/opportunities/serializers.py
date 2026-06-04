from django.utils import timezone
from rest_framework import serializers

from apps.employers.models import Employer
from apps.opportunities.models import Opportunity


class EmployerSummarySerializer(serializers.ModelSerializer):
    """Minimal employer representation for opportunity responses."""

    class Meta:
        model = Employer
        fields = ['id', 'company_name']
        read_only_fields = fields


class OpportunityListSerializer(serializers.ModelSerializer):
    """Serializer used for opportunity list responses."""

    employer = EmployerSummarySerializer(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id',
            'title',
            'employer',
            'employment_type',
            'location',
            'is_remote',
            'currency',
            'salary_min',
            'salary_max',
            'is_featured',
            'deadline',
            'positions_available',
            'views_count',
            'applications_count',
            'created_at',
        ]
        read_only_fields = fields


class OpportunityDetailSerializer(serializers.ModelSerializer):
    """Serializer used for full opportunity detail responses."""

    employer = EmployerSummarySerializer(read_only=True)

    class Meta:
        model = Opportunity
        fields = [
            'id',
            'employer',
            'title',
            'description',
            'requirements',
            'responsibilities',
            'skills_required',
            'experience_level',
            'salary_min',
            'salary_max',
            'currency',
            'is_paid',
            'location',
            'is_remote',
            'employment_type',
            'duration_weeks',
            'start_date',
            'deadline',
            'positions_available',
            'positions_filled',
            'status',
            'is_featured',
            'views_count',
            'applications_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'employer',
            'positions_filled',
            'status',
            'views_count',
            'applications_count',
            'created_at',
            'updated_at',
        ]


class OpportunityCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating opportunities."""

    skills_required = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=True,
        allow_empty=False,
    )

    class Meta:
        model = Opportunity
        fields = [
            'title',
            'description',
            'requirements',
            'responsibilities',
            'skills_required',
            'experience_level',
            'salary_min',
            'salary_max',
            'currency',
            'is_paid',
            'location',
            'is_remote',
            'employment_type',
            'duration_weeks',
            'start_date',
            'deadline',
            'positions_available',
        ]

    def validate_skills_required(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('Skills required must be a list of strings.')
        if not value:
            raise serializers.ValidationError('At least one skill is required.')
        return [str(item).strip() for item in value if str(item).strip()]

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        deadline = attrs.get('deadline')
        positions_available = attrs.get('positions_available')

        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError({'salary_max': 'Maximum salary must be greater than or equal to minimum salary.'})

        if deadline and deadline <= timezone.now():
            raise serializers.ValidationError({'deadline': 'Deadline must be in the future.'})

        if positions_available is not None and positions_available < 1:
            raise serializers.ValidationError({'positions_available': 'There must be at least one position available.'})

        return attrs
