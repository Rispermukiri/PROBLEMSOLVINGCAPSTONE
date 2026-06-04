from rest_framework import serializers

from apps.applications.models import Application
from apps.opportunities.serializers import OpportunityListSerializer
from apps.students.serializers import UserSerializer


class ApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer used when students apply for an opportunity."""

    opportunity_id = serializers.IntegerField(write_only=True)
    cover_letter = serializers.CharField(min_length=50, max_length=2000)

    class Meta:
        model = Application
        fields = ['opportunity_id', 'cover_letter']

    def validate_opportunity_id(self, value):
        from apps.opportunities.models import Opportunity

        try:
            opportunity = Opportunity.objects.get(id=value, is_deleted=False)
        except Opportunity.DoesNotExist:
            raise serializers.ValidationError('Opportunity not found.')

        if not opportunity.can_apply():
            raise serializers.ValidationError('Cannot apply to this opportunity.')

        return value

    def validate(self, attrs):
        student = self.context['student']
        opportunity_id = attrs['opportunity_id']
        if Application.objects.filter(student=student, opportunity_id=opportunity_id).exists():
            raise serializers.ValidationError('You have already applied to this opportunity.')
        return attrs


class ApplicationListSerializer(serializers.ModelSerializer):
    """Serializer used for listing applications for students and employers."""

    opportunity = OpportunityListSerializer(read_only=True)
    student = UserSerializer(source='student.user', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'opportunity',
            'status',
            'rating',
            'applied_at',
            'reviewed_at',
            'decided_at',
        ]
        read_only_fields = fields


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """Serializer used for application detail responses."""

    opportunity = OpportunityListSerializer(read_only=True)
    student = UserSerializer(source='student.user', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'opportunity',
            'cover_letter',
            'cv_snapshot',
            'status',
            'rating',
            'notes',
            'rejection_reason',
            'reviewed_by',
            'reviewed_at',
            'decided_at',
            'withdrawn_at',
            'applied_at',
            'updated_at',
        ]
        read_only_fields = fields
