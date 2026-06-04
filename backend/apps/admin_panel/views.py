"""
Admin panel views for AttachLink.
Handles moderation and admin dashboard operations.
"""

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import FlaggedContent, AdminAction
from apps.users.models import AdminUser


class FlaggedContentListView(views.APIView):
    """
    Flagged content list endpoint (admin only).
    GET: List all flagged content
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List flagged content"""
        try:
            # Check if user is admin
            admin_user = AdminUser.objects.filter(user=request.user).first()
            if not admin_user:
                return Response(
                    {'error': 'Admin access required'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # List flagged content
            status_filter = request.query_params.get('status', 'pending')
            flags = FlaggedContent.objects.filter(status=status_filter).order_by('-created_at')

            return Response({
                'results': [
                    {
                        'id': flag.id,
                        'content_type': 'opportunity' if flag.opportunity else 'employer',
                        'content_title': flag.opportunity.title if flag.opportunity else flag.employer.company_name,
                        'reason': flag.reason,
                        'description': flag.description,
                        'flagged_by': flag.flagged_by.email,
                        'status': flag.status,
                        'created_at': flag.created_at,
                    }
                    for flag in flags
                ]
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ResolveFlagView(views.APIView):
    """
    Resolve flagged content endpoint (admin only).
    POST: Resolve a flagged content item
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, flag_id):
        """Resolve flagged content"""
        try:
            # Check if user is admin
            admin_user = AdminUser.objects.filter(user=request.user).first()
            if not admin_user:
                return Response(
                    {'error': 'Admin access required'},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Get flagged content
            flag = FlaggedContent.objects.get(id=flag_id)

            # Resolve
            action = request.data.get('action_taken', 'none')
            notes = request.data.get('resolution_notes', '')

            flag.resolve(admin_user, action=action, notes=notes)

            # Log action
            AdminAction.objects.create(
                performed_by=request.user,
                action_type='resolve_flag',
                description=f'Resolved flag {flag_id} with action {action}',
            )

            return Response({
                'message': 'Flag resolved successfully',
                'flag': {
                    'id': flag.id,
                    'status': flag.status,
                }
            }, status=status.HTTP_200_OK)

        except FlaggedContent.DoesNotExist:
            return Response(
                {'error': 'Flag not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
