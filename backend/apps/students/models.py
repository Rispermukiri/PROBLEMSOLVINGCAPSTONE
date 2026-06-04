"""
Students App Models
Handles student profiles, CVs, and skills
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
import json


class StudentProfile(models.Model):
    """
    Extended student profile with academic and professional information.
    
    Linked to User with role='student' via OneToOne relationship.
    """
    
    # Relationship to User
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student_profile',
        limit_choices_to={'role': 'student'}
    )
    
    # Academic information
    university = models.CharField(
        max_length=255,
        help_text="Name of the university or institution",
        db_index=True
    )
    major_field = models.CharField(
        max_length=255,
        blank=True,
        help_text="Field of study or major"
    )
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00, "GPA cannot be below 0.00"),
            MaxValueValidator(4.00, "GPA cannot exceed 4.00")
        ],
        help_text="Grade Point Average (0.00 - 4.00)"
    )
    graduation_year = models.IntegerField(
        null=True,
        blank=True,
        help_text="Expected graduation year"
    )
    
    # Professional information
    bio = models.TextField(
        blank=True,
        max_length=1000,
        help_text="Short biography about the student"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Contact phone number"
    )
    
    # Skills and CV
    skills = models.JSONField(
        default=list,
        help_text="JSON array of skills: ['Python', 'React', 'SQL']"
    )
    
    cv_file = models.FileField(
        upload_to='cvs/%Y/%m/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        help_text="CV file (PDF or DOCX, max 5MB)"
    )
    
    cv_uploaded_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When CV was last uploaded"
    )
    
    # Availability and preferences
    is_international = models.BooleanField(
        default=False,
        help_text="International student status"
    )
    
    availability_start = models.DateField(
        null=True,
        blank=True,
        help_text="When available for internship/attachment"
    )
    
    preferred_locations = models.JSONField(
        default=list,
        help_text="JSON array of preferred work locations"
    )
    
    preferred_roles = models.JSONField(
        default=list,
        help_text="JSON array of preferred role types"
    )
    
    # Status
    profile_complete = models.BooleanField(
        default=False,
        help_text="Is profile 100% complete?"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_profile_update = models.DateTimeField(
        auto_now=True,
        help_text="Track when profile was last updated"
    )
    
    class Meta:
        db_table = 'student_profiles'
        verbose_name = 'Student Profile'
        verbose_name_plural = 'Student Profiles'
        indexes = [
            models.Index(fields=['university']),
            models.Index(fields=['profile_complete']),
        ]
    
    def __str__(self):
        return f"Student: {self.user.email}"
    
    def __repr__(self):
        return f"<StudentProfile: {self.user.email}>"
    
    def clean(self):
        """Validate student profile data"""
        # Ensure user is actually a student
        if self.user.role != 'student':
            raise ValidationError("StudentProfile must be linked to a user with role='student'")
        
        # Validate skills is a list
        if not isinstance(self.skills, list):
            raise ValidationError({'skills': 'Skills must be a JSON array'})
        
        # Ensure at least one skill
        if len(self.skills) == 0 and self.profile_complete:
            raise ValidationError({'skills': 'At least one skill is required'})
        
        # Validate GPA is in range
        if not (0.00 <= self.gpa <= 4.00):
            raise ValidationError({'gpa': 'GPA must be between 0.00 and 4.00'})
    
    def save(self, *args, **kwargs):
        """Override save to perform validation and update profile status"""
        self.clean()
        
        # Check if profile is complete
        self._update_profile_completeness()
        
        super().save(*args, **kwargs)
    
    def _update_profile_completeness(self):
        """Check if profile has all required fields"""
        required_fields = [
            self.user_id,
            self.university,
            self.gpa,
            bool(self.skills),  # Has at least one skill
            self.cv_file,  # Has CV uploaded
        ]
        
        self.profile_complete = all(required_fields)
    
    def add_skill(self, skill_name):
        """Add a skill to the student's profile"""
        if skill_name not in self.skills:
            self.skills.append(skill_name)
            self.save(update_fields=['skills'])
    
    def remove_skill(self, skill_name):
        """Remove a skill from the student's profile"""
        if skill_name in self.skills:
            self.skills.remove(skill_name)
            self.save(update_fields=['skills'])
    
    def has_skill(self, skill_name):
        """Check if student has a specific skill"""
        return skill_name in self.skills
    
    def get_skills(self):
        """Get list of skills"""
        return self.skills if self.skills else []
    
    def update_cv(self, new_cv_file):
        """Update CV file"""
        from django.utils import timezone
        self.cv_file = new_cv_file
        self.cv_uploaded_at = timezone.now()
        self.save(update_fields=['cv_file', 'cv_uploaded_at'])
    
    def get_profile_completeness_percentage(self):
        """Calculate profile completeness percentage"""
        checks = {
            'email_verified': self.user.email_verified,
            'university': bool(self.university),
            'gpa': bool(self.gpa),
            'skills': len(self.skills) > 0,
            'cv': bool(self.cv_file),
            'availability': bool(self.availability_start),
        }
        
        completed = sum(1 for v in checks.values() if v)
        total = len(checks)
        return int((completed / total) * 100)
    
    @property
    def can_apply(self):
        """Check if student can apply for opportunities"""
        # Must have email verified, CV, and at least one skill
        return (
            self.user.email_verified
            and self.cv_file
            and len(self.skills) > 0
        )
