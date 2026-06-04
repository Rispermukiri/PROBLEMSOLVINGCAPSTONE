"""
Employers App Models
Handles employer profiles and company information
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone


class Employer(models.Model):
    """
    Employer profile with company information.
    
    Linked to User with role='employer' via OneToOne relationship.
    Must be verified by admin before posting opportunities.
    """
    
    INDUSTRY_CHOICES = (
        ('technology', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('consulting', 'Consulting'),
        ('energy', 'Energy'),
        ('telecommunications', 'Telecommunications'),
        ('other', 'Other'),
    )
    
    # Relationship to User
    user = models.OneToOneField(
        'users.User',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='employer_profile',
        limit_choices_to={'role': 'employer'}
    )
    
    # Company information
    company_name = models.CharField(
        max_length=255,
        unique=False,
        db_index=True,
        help_text="Official company name"
    )
    
    company_logo = models.ImageField(
        upload_to='company_logos/%Y/%m/',
        null=True,
        blank=True,
        help_text="Company logo (max 2MB)"
    )
    
    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES,
        help_text="Company's primary industry"
    )
    
    website = models.URLField(
        blank=True,
        help_text="Company website URL"
    )
    
    description = models.TextField(
        max_length=2000,
        help_text="About the company"
    )
    
    company_size = models.CharField(
        max_length=50,
        choices=[
            ('1-50', '1-50 employees'),
            ('51-200', '51-200 employees'),
            ('201-500', '201-500 employees'),
            ('501-1000', '501-1000 employees'),
            ('1000+', '1000+ employees'),
        ],
        blank=True,
        help_text="Approximate company size"
    )
    
    headquarters_location = models.CharField(
        max_length=255,
        blank=True,
        help_text="HQ location (city, country)"
    )
    
    # Verification by admin
    is_verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Admin must verify before posting opportunities"
    )
    
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When admin verified this employer"
    )
    
    verified_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_employers',
        help_text="Admin who verified this employer"
    )
    
    verification_notes = models.TextField(
        blank=True,
        help_text="Admin notes during verification"
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text="Can post opportunities"
    )
    
    is_banned = models.BooleanField(
        default=False,
        help_text="Banned from posting (due to policy violation)"
    )
    
    ban_reason = models.TextField(
        blank=True,
        help_text="Reason for banning (if applicable)"
    )
    
    # Statistics
    total_postings = models.IntegerField(
        default=0,
        help_text="Total opportunities posted"
    )
    
    total_applications = models.IntegerField(
        default=0,
        help_text="Total applications received"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'employers'
        verbose_name = 'Employer'
        verbose_name_plural = 'Employers'
        indexes = [
            models.Index(fields=['company_name']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        status = "[BANNED]" if self.is_banned else "[UNVERIFIED]" if not self.is_verified else ""
        return f"Employer: {self.company_name} {status}"
    
    def __repr__(self):
        return f"<Employer: {self.company_name}>"
    
    def clean(self):
        """Validate employer data"""
        # Ensure user is actually an employer
        if self.user.role != 'employer':
            raise ValidationError("Employer must be linked to a user with role='employer'")
        
        # Cannot be both banned and active
        if self.is_banned and self.is_active:
            raise ValidationError("Cannot be active if banned")
        
        # Company name required
        if not self.company_name or len(self.company_name.strip()) < 2:
            raise ValidationError({'company_name': 'Company name must be at least 2 characters'})
        
        # Description required
        if not self.description or len(self.description.strip()) < 10:
            raise ValidationError({'description': 'Description must be at least 10 characters'})
    
    def save(self, *args, **kwargs):
        """Override save to perform validation"""
        self.clean()
        super().save(*args, **kwargs)
    
    def verify(self, admin_user, notes=''):
        """
        Mark employer as verified by admin
        
        Args:
            admin_user: User object with role='admin'
            notes: Optional verification notes
        """
        if admin_user.role != 'admin':
            raise ValidationError("Only admins can verify employers")
        
        self.is_verified = True
        self.verified_at = timezone.now()
        self.verified_by = admin_user
        self.verification_notes = notes
        self.save(update_fields=['is_verified', 'verified_at', 'verified_by', 'verification_notes'])
    
    def reject_verification(self, admin_user, reason):
        """
        Reject employer verification and ban them
        
        Args:
            admin_user: User object with role='admin'
            reason: Reason for rejection
        """
        if admin_user.role != 'admin':
            raise ValidationError("Only admins can reject employers")
        
        self.is_banned = True
        self.is_active = False
        self.ban_reason = reason
        self.save(update_fields=['is_banned', 'is_active', 'ban_reason'])
    
    def unban(self):
        """Remove ban from employer"""
        self.is_banned = False
        self.is_active = True
        self.ban_reason = ''
        self.save(update_fields=['is_banned', 'is_active', 'ban_reason'])
    
    def can_post_opportunities(self):
        """Check if employer can post opportunities"""
        return (
            self.is_verified
            and self.is_active
            and not self.is_banned
            and self.user.is_active
        )
    
    def can_review_applications(self):
        """Check if employer can review applications"""
        return self.is_active and self.user.is_active
    
    def increment_postings(self):
        """Increment total postings count"""
        self.total_postings += 1
        self.save(update_fields=['total_postings'])
    
    def increment_applications(self):
        """Increment total applications count"""
        self.total_applications += 1
        self.save(update_fields=['total_applications'])
    
    def get_pending_applications_count(self):
        """Get count of pending applications"""
        from apps.applications.models import Application
        return Application.objects.filter(
            opportunity__employer=self,
            status='pending'
        ).count()
    
    def get_active_opportunities_count(self):
        """Get count of active (open) opportunities"""
        from apps.opportunities.models import Opportunity
        return Opportunity.objects.filter(
            employer=self,
            status='open'
        ).count()
    
    @property
    def verification_status(self):
        """Get human-readable verification status"""
        if self.is_banned:
            return "Banned"
        elif self.is_verified:
            return "Verified"
        else:
            return "Pending Review"
