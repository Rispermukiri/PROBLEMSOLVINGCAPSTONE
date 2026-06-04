"""
Users App Models
Handles authentication, user management, and role-based access control
"""

from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Custom manager for the User model."""

    use_in_migrations = True

    def create_user(self, email, password=None, role='student', **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'admin':
            raise ValueError('Superuser must have role="admin"')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Base User model for authentication and role management.

    Roles:
    - 'student': Can search, apply for opportunities
    - 'employer': Can post opportunities, review applicants
    - 'admin': Can manage users, verify employers, moderate content
    """

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('employer', 'Employer'),
        ('admin', 'Administrator'),
    )

    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, db_index=True, max_length=254)
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        db_index=True,
        help_text='Determines user permissions and profile type',
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Inactive users cannot log in',
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site',
    )
    email_verified = models.BooleanField(
        default=False,
        help_text='Email verification status',
    )
    email_verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When email was verified',
    )

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def __repr__(self):
        return f"<User: {self.email} ({self.role})>"

    def clean(self):
        self.email = self.email.lower().strip()

        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError({'role': f"Invalid role '{self.role}'"})

    def save(self, *args, **kwargs):
        self.clean()

        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def verify_email(self):
        self.email_verified = True
        self.email_verified_at = timezone.now()
        self.save(update_fields=['email_verified', 'email_verified_at'])

    def deactivate(self):
        self.is_active = False
        self.save(update_fields=['is_active'])

    def activate(self):
        self.is_active = True
        self.save(update_fields=['is_active'])

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save(update_fields=['last_login'])

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_employer(self):
        return self.role == 'employer'

    @property
    def is_admin(self):
        return self.role == 'admin'


class AdminUser(models.Model):
    """
    Extended admin user profile for additional admin-specific data.

    Links to User with role='admin'
    """

    PERMISSION_LEVEL_CHOICES = (
        ('moderator', 'Moderator - Can moderate content'),
        ('reviewer', 'Reviewer - Can verify employers'),
        ('super_admin', 'Super Admin - Full access'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='admin_profile',
    )
    permission_level = models.CharField(
        max_length=20,
        choices=PERMISSION_LEVEL_CHOICES,
        default='moderator',
    )
    total_moderation_actions = models.IntegerField(default=0)
    total_verifications = models.IntegerField(default=0)
    total_bans = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_users'
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"Admin: {self.user.email} ({self.permission_level})"

    def clean(self):
        if self.user.role != 'admin':
            raise ValidationError("AdminUser must have role='admin'")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def can_moderate(self):
        return self.permission_level in ['moderator', 'super_admin']

    def can_verify_employer(self):
        return self.permission_level in ['reviewer', 'super_admin']

    def can_manage_users(self):
        return self.permission_level == 'super_admin'
