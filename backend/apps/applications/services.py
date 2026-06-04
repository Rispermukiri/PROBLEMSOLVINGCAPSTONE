from django.utils import timezone
from django.db.models import Q

from apps.applications.models import Application
from apps.students.models import StudentProfile
from apps.opportunities.models import Opportunity


class ApplicationService:
    """Application workflow use cases and query helpers."""

    @staticmethod
    def get_student_profile(user):
        return StudentProfile.objects.select_related('user').get(user=user)

    @staticmethod
    def get_student_applications(student):
        return Application.objects.filter(student=student).select_related('opportunity', 'reviewed_by', 'student__user')

    @staticmethod
    def get_employer_applications(user):
        return Application.objects.filter(
            opportunity__employer__user=user
        ).select_related('opportunity', 'student__user', 'reviewed_by')

    @staticmethod
    def get_application(application_id):
        return Application.objects.select_related('student__user', 'opportunity__employer').get(id=application_id)

    @staticmethod
    def create_application(student, opportunity, cover_letter, cv_snapshot):
        application = Application.objects.create(
            student=student,
            opportunity=opportunity,
            cover_letter=cover_letter,
            cv_snapshot=cv_snapshot,
        )
        opportunity.update_application_count()
        return application

    @staticmethod
    def withdraw_application(application):
        application.withdraw()
        return application

    @staticmethod
    def get_cv_snapshot(student_profile):
        snapshot = {
            'major_field': student_profile.major_field,
            'gpa': float(student_profile.gpa) if student_profile.gpa is not None else None,
            'skills': student_profile.skills,
            'university': student_profile.university,
            'availability_start': student_profile.availability_start.isoformat() if student_profile.availability_start else None,
        }
        if student_profile.cv_file:
            try:
                snapshot['cv_file_url'] = student_profile.cv_file.url
            except Exception:
                snapshot['cv_file_url'] = None
        return snapshot
