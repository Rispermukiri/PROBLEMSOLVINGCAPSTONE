from django.contrib import admin
from .models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'university', 'gpa', 'profile_complete', 'created_at')
    list_filter = ('university', 'profile_complete', 'is_international', 'created_at')
    search_fields = ('user__email', 'university', 'major_field')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('User', {'fields': ('user',)}),
        ('Academic Info', {
            'fields': ('university', 'major_field', 'gpa', 'graduation_year'),
        }),
        ('Professional Info', {
            'fields': ('bio', 'phone', 'skills', 'cv_file', 'cv_uploaded_at'),
        }),
        ('Preferences', {
            'fields': ('is_international', 'availability_start', 'preferred_locations', 'preferred_roles'),
        }),
        ('Status', {
            'fields': ('profile_complete',),
        }),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'
