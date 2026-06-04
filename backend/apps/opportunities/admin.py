from django.contrib import admin
from .models import Opportunity


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer_company', 'employment_type', 'status', 'deadline', 'created_at')
    list_filter = ('status', 'employment_type', 'location', 'is_remote', 'is_featured', 'deadline', 'created_at')
    search_fields = ('title', 'employer__company_name', 'location')
    readonly_fields = ('views_count', 'applications_count', 'created_at', 'updated_at')

    fieldsets = (
        ('Employer', {'fields': ('employer',)}),
        ('Job Details', {
            'fields': ('title', 'description', 'responsibilities', 'requirements'),
        }),
        ('Job Specifications', {
            'fields': ('employment_type', 'experience_level', 'duration_weeks', 'skills_required'),
        }),
        ('Location & Remote', {
            'fields': ('location', 'is_remote'),
        }),
        ('Compensation', {
            'fields': ('is_paid', 'salary_min', 'salary_max', 'currency'),
        }),
        ('Timeline', {
            'fields': ('start_date', 'deadline'),
        }),
        ('Positions', {
            'fields': ('positions_available', 'positions_filled'),
        }),
        ('Status', {
            'fields': ('status', 'is_featured', 'is_deleted'),
        }),
        ('Statistics', {
            'fields': ('views_count', 'applications_count'),
        }),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    def employer_company(self, obj):
        return obj.employer.company_name
    employer_company.short_description = 'Company'
