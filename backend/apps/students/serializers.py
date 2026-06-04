from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.students.models import StudentProfile
from apps.users.serializers import UserSerializer

User = get_user_model()


class StudentProfileSerializer(serializers.ModelSerializer):
    """Serialize and validate student profile data for student self-management."""

    user = UserSerializer(read_only=True)
    skills = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True,
    )
    preferred_locations = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True,
    )
    preferred_roles = serializers.ListField(
        child=serializers.CharField(max_length=100),
        required=False,
        allow_empty=True,
    )
    cv_file = serializers.FileField(required=False, allow_null=True)
    availability_start = serializers.DateField(required=False, allow_null=True)
    graduation_year = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'university',
            'major_field',
            'gpa',
            'graduation_year',
            'bio',
            'phone',
            'skills',
            'cv_file',
            'cv_uploaded_at',
            'is_international',
            'availability_start',
            'preferred_locations',
            'preferred_roles',
            'profile_complete',
            'created_at',
            'updated_at',
            'last_profile_update',
        ]
        read_only_fields = [
            'id',
            'user',
            'cv_uploaded_at',
            'profile_complete',
            'created_at',
            'updated_at',
            'last_profile_update',
        ]
        extra_kwargs = {
            'bio': {'required': False, 'allow_blank': True},
            'phone': {'required': False, 'allow_blank': True},
            'major_field': {'required': False, 'allow_blank': True},
        }

    def validate_skills(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError('Skills must be a list of strings.')
        return value

    def validate_preferred_locations(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError('Preferred locations must be a list.')
        return value

    def validate_preferred_roles(self, value):
        if value is None:
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError('Preferred roles must be a list.')
        return value

    def update(self, instance, validated_data):
        cv_file = validated_data.pop('cv_file', None)
        profile = super().update(instance, validated_data)
        if cv_file is not None:
            profile.update_cv(cv_file)
        return profile


class PublicStudentProfileSerializer(serializers.ModelSerializer):
    """Serialize public student profile data for employer/admin views."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = [
            'id',
            'user',
            'university',
            'major_field',
            'gpa',
            'graduation_year',
            'bio',
            'skills',
            'preferred_locations',
            'preferred_roles',
            'is_international',
            'availability_start',
            'profile_complete',
            'created_at',
        ]
        read_only_fields = fields
