from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, AdminUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'role', 'is_staff', 'is_active', 'email_verified', 'created_at')
    list_filter = ('role', 'is_staff', 'is_active', 'email_verified', 'created_at')
    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'email_verified_at', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'role', 'password1', 'password2', 'is_staff', 'is_active'),
            },
        ),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login', 'email_verified_at')


@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'permission_level', 'total_moderation_actions', 'created_at')
    list_filter = ('permission_level', 'created_at')
    search_fields = ('user__email',)
    readonly_fields = ('total_moderation_actions', 'total_verifications', 'total_bans', 'created_at', 'updated_at')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    fieldsets = (
        (None, {'fields': ('user', 'permission_level')}),
        ('Statistics', {
            'fields': ('total_moderation_actions', 'total_verifications', 'total_bans'),
        }),
        ('Important dates', {'fields': ('created_at', 'updated_at')}),
    )
