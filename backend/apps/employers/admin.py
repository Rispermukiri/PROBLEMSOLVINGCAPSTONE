from django.contrib import admin
from .models import Employer


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user_email', 'is_verified', 'is_active', 'is_banned', 'created_at')
    list_filter = ('is_verified', 'is_active', 'is_banned', 'industry', 'created_at')
    search_fields = ('company_name', 'user__email')
    readonly_fields = ('total_postings', 'total_applications', 'created_at', 'updated_at', 'verified_at')

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Company Info', {
            'fields': ('company_name', 'company_logo', 'industry', 'website', 'description', 'company_size', 'headquarters_location'),
        }),
        ('Verification', {
            'fields': ('is_verified', 'verified_at', 'verified_by', 'verification_notes'),
        }),
        ('Status', {
            'fields': ('is_active', 'is_banned', 'ban_reason'),
        }),
        ('Statistics', {
            'fields': ('total_postings', 'total_applications'),
        }),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
