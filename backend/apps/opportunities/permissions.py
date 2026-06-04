from rest_framework import permissions


class IsOpportunityOwner(permissions.BasePermission):
    """Only the employer who owns an opportunity can modify or delete it."""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == 'employer' and
            obj.employer.user == request.user
        )
