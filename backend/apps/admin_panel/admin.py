from django.contrib import admin
from .models import FlaggedContent, AdminAction


@admin.register(FlaggedContent)
class FlaggedContentAdmin(admin.ModelAdmin):
    list_display = ('flagged_content_type', 'reason', 'status', 'flagged_by_email', 'created_at')
    list_filter = ('status', 'reason', 'action_taken', 'created_at')
    search_fields = ('flagged_by__email', 'description')
    readonly_fields = ('created_at', 'updated_at', 'resolved_at')

    fieldsets = (
        ('Flagged Content', {'fields': ('opportunity', 'employer')}),
        ('Flag Details', {
            'fields': ('flagged_by', 'reason', 'description'),
        }),
        ('Resolution', {
            'fields': ('status', 'action_taken', 'resolution_notes', 'resolved_by'),
        }),
        ('Important dates', {'fields': ('created_at', 'updated_at', 'resolved_at')}),
    )

    def flagged_content_type(self, obj):
        if obj.opportunity:
            return f"Opportunity: {obj.opportunity.title}"
        elif obj.employer:
            return f"Employer: {obj.employer.company_name}"
        return "Unknown"
    flagged_content_type.short_description = 'Flagged Content'

    def flagged_by_email(self, obj):
        return obj.flagged_by.email
    flagged_by_email.short_description = 'Flagged By'


@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'performed_by_email', 'description', 'created_at')
    list_filter = ('action_type', 'created_at')
    search_fields = ('performed_by__email', 'description')
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Admin Action', {
            'fields': ('performed_by', 'action_type'),
        }),
        ('Details', {
            'fields': ('description', 'employer', 'user', 'opportunity'),
        }),
        ('Important dates', {'fields': ('created_at',)}),
    )

    def performed_by_email(self, obj):
        return obj.performed_by.email
    performed_by_email.short_description = 'Performed By'
