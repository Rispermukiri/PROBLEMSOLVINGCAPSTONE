"""
Applications App Models
Handles student applications for opportunities
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Application(models.Model):
    """
    Track student applications for opportunities.
    
    Core model for the hiring workflow. Each application:
    1. Student applies
    2. Employer reviews
    3. Employer accepts/rejects
    4. Status is tracked and updated
    """
    
    STATUS_CHOICES = (
        ('pending', 'Pending - Awaiting review'),
        ('reviewed', 'Reviewed - Under consideration'),
        ('accepted', 'Accepted - Offered position'),
        ('rejected', 'Rejected - Not selected'),
        ('withdrawn', 'Withdrawn - Student withdrew'),
    )
    
    # Relationships
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='applications',
        help_text="Student who applied"
    )
    
    opportunity = models.ForeignKey(
        'opportunities.Opportunity',
        on_delete=models.CASCADE,
        related_name='applications',
        help_text="Opportunity applied for"
    )
    
    # Relationship to reviewer (employer or admin)
    reviewed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications_reviewed',
        help_text="Who reviewed/decided on this application"
    )
    
    # Application content
    cover_letter = models.TextField(
        help_text="Student's motivational message (50-2000 characters)"
    )
    
    cv_snapshot = models.JSONField(
        default=dict,
        blank=True,
        help_text="Snapshot of student's CV data at time of application"
    )
    
    # Employer feedback
    rating = models.IntegerField(
        null=True,
        blank=True,
        choices=[(i, f"{i} Star{'s' if i != 1 else ''}") for i in range(1, 6)],
        help_text="Employer's rating of applicant (1-5 stars)"
    )
    
    notes = models.TextField(
        blank=True,
        help_text="Employer's internal notes about applicant"
    )
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        help_text="Current application status"
    )
    
    rejection_reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Reason for rejection (if applicable)"
    )
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When first reviewed by employer"
    )
    decided_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When accept/reject decision was made"
    )
    withdrawn_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When student withdrew (if applicable)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'applications'
        ordering = ['-applied_at']
        
        # Prevent duplicate applications from same student to same opportunity
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'opportunity'],
                name='unique_student_opportunity_application'
            )
        ]
        
        indexes = [
            models.Index(fields=['student', 'status']),
            models.Index(fields=['opportunity', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['applied_at']),
            models.Index(fields=['decided_at']),
        ]
        
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
    
    def __str__(self):
        return f"{self.student.user.email} → {self.opportunity.title}"
    
    def __repr__(self):
        return f"<Application: {self.student.user.email} @ {self.opportunity.title} ({self.status})>"
    
    def clean(self):
        """Validate application data"""
        # Cover letter validation
        if not self.cover_letter or len(self.cover_letter.strip()) < 50:
            raise ValidationError({'cover_letter': 'Cover letter must be at least 50 characters'})
        
        if len(self.cover_letter.strip()) > 2000:
            raise ValidationError({'cover_letter': 'Cover letter cannot exceed 2000 characters'})
        
        # Status validation
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError({'status': f"Invalid status '{self.status}'"})
        
        # Rating validation
        if self.rating and not (1 <= self.rating <= 5):
            raise ValidationError({'rating': 'Rating must be between 1 and 5'})
        
        # Ensure student can apply for opportunity
        if not self.opportunity.can_apply():
            raise ValidationError("Opportunity is no longer accepting applications")
    
    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=exclude)
        if Application.objects.filter(student=self.student, opportunity=self.opportunity).exclude(pk=self.pk).exists():
            raise ValidationError({'__all__': 'You have already applied to this opportunity.'})

    def save(self, *args, **kwargs):
        """Override save to perform validation"""
        self.clean()
        self.validate_unique()
        super().save(*args, **kwargs)

    def mark_as_reviewed(self, reviewer_user):
        """
        Mark application as reviewed by employer/admin
        
        Args:
            reviewer_user: User object of the reviewer
        """
        if self.status == 'pending':
            self.status = 'reviewed'
        
        self.reviewed_by = reviewer_user
        self.reviewed_at = timezone.now()
        self.save(update_fields=['status', 'reviewed_by', 'reviewed_at'])
    
    def accept(self, reviewer_user, notes=''):
        """
        Accept the application and offer position
        
        Args:
            reviewer_user: User object of the employer/admin
            notes: Optional notes
        """
        self.status = 'accepted'
        self.reviewed_by = reviewer_user
        self.decided_at = timezone.now()
        
        if notes:
            self.notes = notes
        
        # Increment opportunity positions filled
        self.opportunity.increment_positions_filled()
        
        self.save(update_fields=['status', 'reviewed_by', 'decided_at', 'notes'])
    
    def reject(self, reviewer_user, reason='', notes=''):
        """
        Reject the application
        
        Args:
            reviewer_user: User object of the employer/admin
            reason: Reason for rejection
            notes: Optional internal notes
        """
        self.status = 'rejected'
        self.reviewed_by = reviewer_user
        self.decided_at = timezone.now()
        self.rejection_reason = reason
        
        if notes:
            self.notes = notes
        
        self.save(update_fields=['status', 'reviewed_by', 'decided_at', 'rejection_reason', 'notes'])
    
    def withdraw(self):
        """Student withdraws their application"""
        if self.status not in ['pending', 'reviewed']:
            raise ValidationError("Cannot withdraw from accepted/rejected applications")
        
        self.status = 'withdrawn'
        self.withdrawn_at = timezone.now()
        self.save(update_fields=['status', 'withdrawn_at'])
    
    def set_rating(self, rating, notes=''):
        """
        Set employer rating for this applicant
        
        Args:
            rating: 1-5 star rating
            notes: Optional feedback
        """
        if not (1 <= rating <= 5):
            raise ValidationError("Rating must be between 1 and 5")
        
        self.rating = rating
        if notes:
            self.notes = notes
        self.save(update_fields=['rating', 'notes'])
    
    @property
    def is_pending(self):
        """Check if application is still pending"""
        return self.status == 'pending'
    
    @property
    def is_reviewed(self):
        """Check if application has been reviewed"""
        return self.status in ['reviewed', 'accepted', 'rejected']
    
    @property
    def is_accepted(self):
        """Check if application was accepted"""
        return self.status == 'accepted'
    
    @property
    def is_rejected(self):
        """Check if application was rejected"""
        return self.status == 'rejected'
    
    @property
    def is_withdrawn(self):
        """Check if application was withdrawn"""
        return self.status == 'withdrawn'
    
    @property
    def is_active(self):
        """Check if application is still active (not withdrawn or decided)"""
        return self.status in ['pending', 'reviewed']
    
    @property
    def days_since_application(self):
        """Get number of days since application"""
        delta = timezone.now() - self.applied_at
        return delta.days
    
    @property
    def days_since_review(self):
        """Get number of days since first review"""
        if not self.reviewed_at:
            return None
        delta = timezone.now() - self.reviewed_at
        return delta.days
    
    def get_status_display_friendly(self):
        """Get friendly status display"""
        status_map = {
            'pending': '⏳ Pending Review',
            'reviewed': '👀 Under Review',
            'accepted': '✅ Accepted',
            'rejected': '❌ Rejected',
            'withdrawn': '↩️ Withdrawn',
        }
        return status_map.get(self.status, self.status)
    
    def send_confirmation_email(self):
        """Send confirmation email to student (implement with email service)"""
        # TODO: Implement email sending
        pass
    
    def send_decision_email(self):
        """Send decision email to student (implement with email service)"""
        # TODO: Implement email sending
        pass
