from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student_email', 'opportunity_title', 'status', 'rating', 'applied_at')
    list_filter = ('status', 'rating', 'applied_at', 'reviewed_at', 'decided_at')
    search_fields = ('student__user__email', 'opportunity__title')
    readonly_fields = ('applied_at', 'reviewed_at', 'decided_at', 'withdrawn_at')

    fieldsets = (
        ('Application Info', {'fields': ('student', 'opportunity')}),
        ('Application Content', {'fields': ('cover_letter', 'cv_snapshot')}),
        ('Review', {
            'fields': ('reviewed_by', 'status', 'rating', 'notes'),
        }),
        ('Decision', {
            'fields': ('rejection_reason',),
        }),
        ('Important dates', {'fields': ('applied_at', 'reviewed_at', 'decided_at', 'withdrawn_at')}),
    )

    def student_email(self, obj):
        return obj.student.user.email
    student_email.short_description = 'Student Email'

    def opportunity_title(self, obj):
        return obj.opportunity.title
    opportunity_title.short_description = 'Opportunity'
