from rest_framework import permissions


class IsApplicationOwner(permissions.BasePermission):
    """Allow application owners (students) to access their own applications."""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.student.user == request.user
        )


class IsOpportunityOwner(permissions.BasePermission):
    """Allow opportunity owners (employers) to access applications for their own opportunities."""

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.is_authenticated and
            obj.opportunity.employer.user == request.user
        )
