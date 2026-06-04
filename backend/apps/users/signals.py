"""
Django signals for Users app.
Handles events like user creation, profile auto-creation, etc.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, AdminUser
from apps.students.models import StudentProfile
from apps.employers.models import Employer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create corresponding profile when user is created.
    - Student role -> Create StudentProfile
    - Employer role -> Create Employer
    - Admin role -> Create AdminUser
    """
    if created:
        if instance.role == 'student':
            StudentProfile.objects.get_or_create(user=instance)

        elif instance.role == 'employer':
            Employer.objects.get_or_create(user=instance)

        elif instance.role == 'admin':
            AdminUser.objects.get_or_create(user=instance)
