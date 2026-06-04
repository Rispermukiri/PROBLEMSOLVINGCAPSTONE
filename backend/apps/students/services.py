"""Student profile use cases and business rules.

This module implements application-specific operations for the StudentProfile
aggregate, keeping controller logic thin and preserving clean architecture
boundaries.
"""

from django.utils import timezone

from apps.students.models import StudentProfile


class StudentProfileService:
    """Encapsulate student profile retrieval and update use cases."""

    @staticmethod
    def get_profile_for_user(user):
        """Return the profile for the authenticated student user."""
        return StudentProfile.objects.select_related('user').get(user=user)

    @staticmethod
    def get_profile_by_id(student_id):
        """Return a public student profile by profile ID."""
        return StudentProfile.objects.select_related('user').get(id=student_id)

    @staticmethod
    def update_profile(profile, validated_data):
        """Apply validated updates to a student profile and persist changes."""
        cv_file = validated_data.pop('cv_file', None)

        for attr, value in validated_data.items():
            setattr(profile, attr, value)

        if cv_file is not None:
            profile.cv_file = cv_file
            profile.cv_uploaded_at = timezone.now()

        profile.full_clean()
        profile.save()

        return profile
