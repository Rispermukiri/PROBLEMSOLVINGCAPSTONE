"""
Custom permission classes for AttachLink API.
"""

from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    """
    Allows access only to students.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'student'
        )


class IsEmployer(permissions.BasePermission):
    """
    Allows access only to employers.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'employer'
        )


class IsEmployerOrAdmin(permissions.BasePermission):
    """
    Allows access only to employers or admins.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['employer', 'admin']
        )


class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admins.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'admin'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allows access to owner or admin.
    """
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user or
            request.user.role == 'admin'
        )


class IsVerifiedEmployer(permissions.BasePermission):
    """
    Allows access only to verified employers.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.role == 'employer'):
            return False

        from apps.employers.models import Employer
        try:
            employer = Employer.objects.get(user=request.user)
            return employer.is_verified and not employer.is_banned
        except Employer.DoesNotExist:
            return False
