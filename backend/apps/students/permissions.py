"""Student-specific permissions for the Students app."""

from rest_framework import permissions


class IsStudentProfileOwner(permissions.BasePermission):
    """Allow access only to the owner of the student profile."""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.user == request.user
        )


class IsStudentProfileVisibleToEmployerOrAdmin(permissions.BasePermission):
    """Allow employers and admins to view a student's public profile."""

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['employer', 'admin']
        )
