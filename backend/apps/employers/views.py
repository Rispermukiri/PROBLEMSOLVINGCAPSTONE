"""
Employer profile views for AttachLink.
Handles employer profile CRUD operations.
"""

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Employer


class EmployerProfileView(views.APIView):
    """
    Employer profile endpoint.
    GET: Get current user's employer profile
    PUT: Update current user's employer profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current user's employer profile"""
        try:
            profile = Employer.objects.get(user=request.user)
            return Response({
                'id': profile.id,
                'company_name': profile.company_name,
                'industry': profile.industry,
                'website': profile.website,
                'description': profile.description,
                'company_size': profile.company_size,
                'headquarters_location': profile.headquarters_location,
                'is_verified': profile.is_verified,
                'is_active': profile.is_active,
                'is_banned': profile.is_banned,
                'total_postings': profile.total_postings,
                'total_applications': profile.total_applications,
                'created_at': profile.created_at,
                'updated_at': profile.updated_at,
            }, status=status.HTTP_200_OK)

        except Employer.DoesNotExist:
            return Response(
                {'error': 'Employer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request):
        """Update current user's employer profile"""
        try:
            profile = Employer.objects.get(user=request.user)

            # Update profile fields
            profile.company_name = request.data.get('company_name', profile.company_name)
            profile.industry = request.data.get('industry', profile.industry)
            profile.website = request.data.get('website', profile.website)
            profile.description = request.data.get('description', profile.description)
            profile.company_size = request.data.get('company_size', profile.company_size)
            profile.headquarters_location = request.data.get('headquarters_location', profile.headquarters_location)

            if 'company_logo' in request.FILES:
                profile.company_logo = request.FILES['company_logo']

            profile.full_clean()
            profile.save()

            return Response({
                'message': 'Profile updated successfully',
                'profile': {
                    'id': profile.id,
                    'company_name': profile.company_name,
                    'is_verified': profile.is_verified,
                }
            }, status=status.HTTP_200_OK)

        except Employer.DoesNotExist:
            return Response(
                {'error': 'Employer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class EmployerProfileDetailView(views.APIView):
    """
    Employer profile detail endpoint.
    GET: Get specific employer's profile
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, employer_id):
        """Get specific employer profile"""
        try:
            profile = Employer.objects.get(id=employer_id)

            return Response({
                'id': profile.id,
                'user': {
                    'id': profile.user.id,
                    'email': profile.user.email,
                },
                'company_name': profile.company_name,
                'industry': profile.industry,
                'website': profile.website,
                'description': profile.description,
                'company_size': profile.company_size,
                'headquarters_location': profile.headquarters_location,
                'is_verified': profile.is_verified,
                'total_postings': profile.total_postings,
                'created_at': profile.created_at,
            }, status=status.HTTP_200_OK)

        except Employer.DoesNotExist:
            return Response(
                {'error': 'Employer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
