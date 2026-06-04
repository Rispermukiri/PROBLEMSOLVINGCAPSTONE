"""
Opportunities App Models
Handles internship and attachment opportunity postings
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Opportunity(models.Model):
    """
    Internship/Attachment opportunity posting by employers.
    
    Searchable, filterable, and trackable by students.
    """
    
    EMPLOYMENT_TYPE_CHOICES = (
        ('internship', 'Internship'),
        ('attachment', 'Attachment'),
        ('graduate_program', 'Graduate Program'),
    )
    
    STATUS_CHOICES = (
        ('open', 'Open - Accepting applications'),
        ('closed', 'Closed - Not accepting applications'),
        ('expired', 'Expired - Deadline passed'),
        ('filled', 'Filled - All positions filled'),
    )
    
    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry Level (No experience)'),
        ('intermediate', 'Intermediate (1-2 years)'),
        ('advanced', 'Advanced (3+ years)'),
    )
    
    # Relationship
    employer = models.ForeignKey(
        'employers.Employer',
        on_delete=models.CASCADE,
        related_name='opportunities',
        help_text="Company posting this opportunity"
    )
    
    # Basic information
    title = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Job title (e.g., 'Python Developer Internship')"
    )
    
    description = models.TextField(
        help_text="Detailed description of the role"
    )
    
    requirements = models.TextField(
        help_text="Required qualifications and skills"
    )
    
    responsibilities = models.TextField(
        blank=True,
        help_text="Key responsibilities"
    )
    
    # Skills and experience
    skills_required = models.JSONField(
        default=list,
        help_text="JSON array of required skills: ['Python', 'Django', 'SQL']"
    )
    
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        default='entry',
        help_text="Required experience level"
    )
    
    # Compensation
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Minimum compensation (stipend/salary)"
    )
    
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Maximum compensation"
    )
    
    currency = models.CharField(
        max_length=10,
        choices=[
            ('USD', 'US Dollar'),
            ('KES', 'Kenyan Shilling'),
            ('GBP', 'British Pound'),
            ('EUR', 'Euro'),
            ('CAD', 'Canadian Dollar'),
            ('AUD', 'Australian Dollar'),
        ],
        default='USD',
        help_text="Currency for salary range"
    )
    
    is_paid = models.BooleanField(
        default=True,
        help_text="Is this a paid opportunity?"
    )
    
    # Location and timing
    location = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Job location (city/country)"
    )
    
    is_remote = models.BooleanField(
        default=False,
        help_text="Is this a remote opportunity?"
    )
    
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='internship',
        help_text="Type of opportunity"
    )
    
    duration_weeks = models.IntegerField(
        null=True,
        blank=True,
        help_text="Duration in weeks"
    )
    
    start_date = models.DateField(
        null=True,
        blank=True,
        help_text="Expected start date"
    )
    
    deadline = models.DateTimeField(
        help_text="Application deadline"
    )
    
    # Positions and status
    positions_available = models.IntegerField(
        default=1,
        help_text="Number of positions available"
    )
    
    positions_filled = models.IntegerField(
        default=0,
        help_text="Number of positions filled"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        db_index=True,
        help_text="Current status of the opportunity"
    )
    
    # Discovery and engagement
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured at top of listings"
    )
    
    views_count = models.IntegerField(
        default=0,
        help_text="Number of times viewed"
    )
    
    applications_count = models.IntegerField(
        default=0,
        help_text="Number of applications received"
    )
    
    # Content moderation
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'opportunities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['employer', 'status']),
            models.Index(fields=['location']),
            models.Index(fields=['employment_type']),
            models.Index(fields=['deadline']),
            models.Index(fields=['is_featured']),
        ]
        verbose_name = 'Opportunity'
        verbose_name_plural = 'Opportunities'
    
    def __str__(self):
        return f"{self.title} at {self.employer.company_name}"
    
    def __repr__(self):
        return f"<Opportunity: {self.title} ({self.id})>"
    
    def clean(self):
        """Validate opportunity data"""
        # Title validation
        if not self.title or len(self.title.strip()) < 5:
            raise ValidationError({'title': 'Title must be at least 5 characters'})
        
        # Description validation
        if not self.description or len(self.description.strip()) < 50:
            raise ValidationError({'description': 'Description must be at least 50 characters'})
        
        # Deadline must be in future
        if self.deadline <= timezone.now():
            raise ValidationError({'deadline': 'Deadline must be in the future'})
        
        # Salary validation
        if self.salary_min and self.salary_max:
            if self.salary_min > self.salary_max:
                raise ValidationError({'salary_max': 'Max salary must be >= min salary'})
        
        # Positions validation
        if self.positions_available < 1:
            raise ValidationError({'positions_available': 'Must have at least 1 position'})
        
        if self.positions_filled > self.positions_available:
            raise ValidationError({'positions_filled': 'Filled cannot exceed available'})
        
        # Skills validation
        if not isinstance(self.skills_required, list):
            raise ValidationError({'skills_required': 'Skills must be a JSON array'})
        
        if len(self.skills_required) == 0:
            raise ValidationError({'skills_required': 'At least one skill is required'})
    
    def save(self, *args, **kwargs):
        """Override save to validate and update status"""
        self.clean()
        
        # Auto-update status
        self._update_status()
        
        super().save(*args, **kwargs)
    
    def _update_status(self):
        """Auto-update status based on deadline and positions"""
        if self.is_deleted:
            return
        
        now = timezone.now()
        
        # Check if deadline has passed
        if self.deadline <= now:
            self.status = 'expired'
        # Check if all positions are filled
        elif self.positions_filled >= self.positions_available:
            self.status = 'filled'
        # Otherwise, use current status
    
    def update_view_count(self, increment=1):
        """Increment view count"""
        self.views_count += increment
        self.save(update_fields=['views_count'])
    
    def update_application_count(self, increment=1):
        """Increment application count"""
        self.applications_count += increment
        self.save(update_fields=['applications_count'])
    
    def increment_positions_filled(self):
        """Mark a position as filled"""
        if self.positions_filled < self.positions_available:
            self.positions_filled += 1
            
            # Check if all filled
            if self.positions_filled >= self.positions_available:
                self.status = 'filled'
            
            self.save(update_fields=['positions_filled', 'status'])
    
    def close(self):
        """Manually close the opportunity"""
        self.status = 'closed'
        self.save(update_fields=['status'])
    
    def reopen(self):
        """Reopen a closed opportunity"""
        if self.deadline > timezone.now():
            self.status = 'open'
            self.save(update_fields=['status'])
    
    def soft_delete(self):
        """Soft delete (mark as deleted but keep data)"""
        self.is_deleted = True
        self.status = 'closed'
        self.save(update_fields=['is_deleted', 'status'])
    
    def can_apply(self):
        """Check if students can still apply"""
        return (
            self.status == 'open'
            and self.deadline > timezone.now()
            and self.positions_filled < self.positions_available
            and not self.is_deleted
        )
    
    def is_deadline_soon(self, days=7):
        """Check if deadline is within N days"""
        days_until = (self.deadline - timezone.now()).days
        return 0 <= days_until <= days
    
    def get_salary_display(self):
        """Get formatted salary range"""
        if not self.is_paid:
            return "Unpaid"
        
        if self.salary_min and self.salary_max:
            return f"{self.currency} {self.salary_min} - {self.salary_max}"
        elif self.salary_min:
            return f"{self.currency} {self.salary_min}+"
        elif self.salary_max:
            return f"Up to {self.currency} {self.salary_max}"
        else:
            return "Salary not specified"
    
    @property
    def days_until_deadline(self):
        """Get days remaining until deadline"""
        delta = self.deadline - timezone.now()
        return delta.days
    
    @property
    def is_full(self):
        """Check if all positions are filled"""
        return self.positions_filled >= self.positions_available
