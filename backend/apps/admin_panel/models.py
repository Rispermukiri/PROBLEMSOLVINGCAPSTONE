"""
Admin Panel Models
Handles admin-specific functions like moderation and reporting
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class FlaggedContent(models.Model):
    """
    Content moderation model for flagging inappropriate opportunities or employers.
    
    Used by admins to track reports and take action.
    """
    
    REASON_CHOICES = (
        ('spam', 'Spam - Repetitive or unsolicited'),
        ('inappropriate', 'Inappropriate - Offensive or discriminatory content'),
        ('scam', 'Scam - Appears to be fraudulent'),
        ('duplicate', 'Duplicate - Already posted elsewhere'),
        ('low_quality', 'Low Quality - Lacks detail or professionalism'),
        ('fake_company', 'Fake Company - Company verification failed'),
        ('expired', 'Expired - Opportunity deadline passed'),
        ('other', 'Other - Specify in description'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending - Awaiting admin review'),
        ('reviewed', 'Reviewed - Admin reviewed'),
        ('resolved', 'Resolved - Action taken'),
        ('dismissed', 'Dismissed - False report'),
    )
    
    ACTION_CHOICES = (
        ('none', 'No action taken'),
        ('warning', 'Warning issued to employer'),
        ('remove_content', 'Content removed'),
        ('suspend_account', 'Account suspended'),
        ('ban_account', 'Account banned'),
        ('restore_content', 'Content restored'),
    )
    
    # What is being flagged (one must be set)
    opportunity = models.ForeignKey(
        'opportunities.Opportunity',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='flags',
        help_text="Flagged opportunity (if applicable)"
    )
    
    employer = models.ForeignKey(
        'employers.Employer',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='flags',
        help_text="Flagged employer (if applicable)"
    )
    
    # Who flagged it
    flagged_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='flags_created',
        help_text="User who reported the content"
    )
    
    # Flag details
    reason = models.CharField(
        max_length=50,
        choices=REASON_CHOICES,
        help_text="Reason for flagging"
    )
    
    description = models.TextField(
        max_length=1000,
        help_text="Detailed explanation of why content was flagged"
    )
    
    # Admin resolution
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True,
        help_text="Current status"
    )
    
    action_taken = models.CharField(
        max_length=50,
        choices=ACTION_CHOICES,
        default='none',
        help_text="Action taken by admin"
    )
    
    resolution_notes = models.TextField(
        blank=True,
        help_text="Admin notes on how issue was resolved"
    )
    
    resolved_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='flags_resolved',
        help_text="Admin who resolved this flag"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When flag was resolved"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'flagged_content'
        ordering = ['-created_at']
        
        # Ensure either opportunity or employer is set
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(opportunity__isnull=False, employer__isnull=True) |
                    models.Q(opportunity__isnull=True, employer__isnull=False)
                ),
                name='either_opportunity_or_employer_flagged'
            )
        ]
        
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['reason']),
            models.Index(fields=['created_at']),
        ]
        
        verbose_name = 'Flagged Content'
        verbose_name_plural = 'Flagged Content'
    
    def __str__(self):
        if self.opportunity:
            return f"Flag: {self.opportunity.title} ({self.reason})"
        elif self.employer:
            return f"Flag: {self.employer.company_name} ({self.reason})"
        return f"Flag #{self.id} ({self.reason})"
    
    def __repr__(self):
        if self.opportunity:
            return f"<FlaggedContent: Opportunity #{self.opportunity.id} - {self.reason}>"
        return f"<FlaggedContent: Employer #{self.employer.id} - {self.reason}>"
    
    def clean(self):
        """Validate flag data"""
        # Must have either opportunity or employer, not both
        if not self.opportunity and not self.employer:
            raise ValidationError("Must flag either an opportunity or an employer")
        
        if self.opportunity and self.employer:
            raise ValidationError("Cannot flag both opportunity and employer")
        
        # Description required
        if not self.description or len(self.description.strip()) < 10:
            raise ValidationError({'description': 'Description must be at least 10 characters'})
        
        # If resolved, need resolution notes
        if self.status == 'resolved' and not self.resolution_notes:
            raise ValidationError({'resolution_notes': 'Resolution notes required when marking as resolved'})
    
    def save(self, *args, **kwargs):
        """Override save to perform validation"""
        self.clean()
        super().save(*args, **kwargs)
    
    def mark_as_reviewed(self):
        """Mark flag as reviewed by admin"""
        if self.status == 'pending':
            self.status = 'reviewed'
            self.save(update_fields=['status'])
    
    def resolve(self, admin_user, action, notes):
        """
        Resolve the flag with admin action
        
        Args:
            admin_user: Admin User object
            action: One of ACTION_CHOICES
            notes: Resolution notes
        """
        if admin_user.role != 'admin':
            raise ValidationError("Only admins can resolve flags")
        
        self.status = 'resolved'
        self.action_taken = action
        self.resolution_notes = notes
        self.resolved_by = admin_user
        self.resolved_at = timezone.now()
        
        self.save(update_fields=[
            'status', 'action_taken', 'resolution_notes', 
            'resolved_by', 'resolved_at'
        ])
        
        # Perform the action
        self._perform_action(action)
    
    def dismiss(self, admin_user):
        """
        Dismiss flag as false report
        
        Args:
            admin_user: Admin User object
        """
        if admin_user.role != 'admin':
            raise ValidationError("Only admins can dismiss flags")
        
        self.status = 'dismissed'
        self.action_taken = 'none'
        self.resolved_by = admin_user
        self.resolved_at = timezone.now()
        self.save(update_fields=['status', 'action_taken', 'resolved_by', 'resolved_at'])
    
    def _perform_action(self, action):
        """Execute the action associated with flag resolution"""
        if action == 'remove_content':
            if self.opportunity:
                self.opportunity.soft_delete()
        
        elif action == 'suspend_account':
            if self.employer:
                self.employer.is_active = False
                self.employer.save(update_fields=['is_active'])
        
        elif action == 'ban_account':
            if self.employer:
                self.employer.is_banned = True
                self.employer.is_active = False
                self.employer.save(update_fields=['is_banned', 'is_active'])
        
        elif action == 'restore_content':
            if self.opportunity:
                self.opportunity.is_deleted = False
                self.opportunity.save(update_fields=['is_deleted'])
        
        # For 'warning' and 'none', no automated action needed
    
    @property
    def is_pending(self):
        """Check if flag is pending review"""
        return self.status == 'pending'
    
    @property
    def is_resolved(self):
        """Check if flag is resolved"""
        return self.status == 'resolved'
    
    @property
    def days_since_flag(self):
        """Get days since flag was created"""
        delta = timezone.now() - self.created_at
        return delta.days
    
    @property
    def days_since_resolution(self):
        """Get days since flag was resolved"""
        if not self.resolved_at:
            return None
        delta = timezone.now() - self.resolved_at
        return delta.days


class AdminAction(models.Model):
    """
    Audit log for admin actions.
    
    Tracks all significant admin actions for compliance and auditing.
    """
    
    ACTION_TYPE_CHOICES = (
        ('verify_employer', 'Verify Employer'),
        ('reject_employer', 'Reject Employer'),
        ('ban_user', 'Ban User'),
        ('unban_user', 'Unban User'),
        ('remove_opportunity', 'Remove Opportunity'),
        ('restore_opportunity', 'Restore Opportunity'),
        ('flag_content', 'Flag Content'),
        ('dismiss_flag', 'Dismiss Flag'),
        ('other', 'Other'),
    )
    
    # Who performed action
    performed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='admin_actions',
        help_text="Admin who performed action"
    )
    
    # Action details
    action_type = models.CharField(
        max_length=50,
        choices=ACTION_TYPE_CHOICES,
        help_text="Type of admin action"
    )
    
    description = models.TextField(
        help_text="Description of the action"
    )
    
    # Related objects (one should be set)
    employer_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Employer ID if action related to employer"
    )
    
    user_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="User ID if action related to user"
    )
    
    opportunity_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text="Opportunity ID if action related to opportunity"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'admin_actions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['action_type']),
            models.Index(fields=['performed_by']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Admin Action'
        verbose_name_plural = 'Admin Actions'
    
    def __str__(self):
        return f"{self.get_action_type_display()} by {self.performed_by.email}"
    
    def __repr__(self):
        return f"<AdminAction: {self.action_type} by {self.performed_by.email}>"
