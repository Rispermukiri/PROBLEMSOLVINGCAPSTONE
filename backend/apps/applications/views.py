"""
Application views for AttachLink.
Handles student application workflow and employer applicant review.
"""

from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.applications.models import Application
from apps.applications.permissions import IsApplicationOwner, IsOpportunityOwner
from apps.applications.serializers import (
    ApplicationCreateSerializer,
    ApplicationDetailSerializer,
    ApplicationListSerializer,
)
from apps.applications.services import ApplicationService
from utils.permissions import IsStudent


class ApplicationsListView(views.APIView):
    """List applications for authenticated students and employers."""
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        operation_id='list_applications',
        description='List applications for the authenticated student or employer.',
        responses=ApplicationListSerializer,
    )
    def get(self, request):
        student = None
        try:
            student = ApplicationService.get_student_profile(request.user)
        except Exception:
            pass

        if student:
            applications = ApplicationService.get_student_applications(student).order_by('-applied_at')
            serializer = ApplicationListSerializer(applications, many=True)
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)

        if request.user.role == 'employer':
            applications = ApplicationService.get_employer_applications(request.user).order_by('-applied_at')
            serializer = ApplicationListSerializer(applications, many=True)
            return Response({'results': serializer.data}, status=status.HTTP_200_OK)

        return Response(
            {'detail': 'Not authorized to view applications.'},
            status=status.HTTP_403_FORBIDDEN,
        )


class ApplyView(generics.CreateAPIView):
    """Submit an application to an opportunity (student only)."""
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    @extend_schema(
        operation_id='apply_to_opportunity',
        description='Submit an application for an open opportunity. Students may apply only once per opportunity.',
        request=ApplicationCreateSerializer,
        responses=ApplicationDetailSerializer,
    )
    def create(self, request, *args, **kwargs):
        try:
            student = ApplicationService.get_student_profile(request.user)
        except Exception:
            return Response(
                {'detail': 'Student profile not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(data=request.data, context={'student': student})
        serializer.is_valid(raise_exception=True)

        from apps.opportunities.models import Opportunity

        opportunity = Opportunity.objects.get(id=serializer.validated_data['opportunity_id'])
        cv_snapshot = ApplicationService.get_cv_snapshot(student)
        application = ApplicationService.create_application(
            student=student,
            opportunity=opportunity,
            cover_letter=serializer.validated_data['cover_letter'],
            cv_snapshot=cv_snapshot,
        )

        output = ApplicationDetailSerializer(application)
        return Response(output.data, status=status.HTTP_201_CREATED)


class ApplicationDetailView(generics.RetrieveAPIView):
    """Retrieve a single application for the applicant or opportunity owner."""
    queryset = Application.objects.select_related('student__user', 'opportunity__employer', 'reviewed_by')
    serializer_class = ApplicationDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'application_id'

    @extend_schema(
        operation_id='retrieve_application',
        description='Retrieve application details for the applicant or the employer owning the opportunity.',
        responses=ApplicationDetailSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        application = self.get_object()
        if not (IsApplicationOwner().has_object_permission(request, self, application)
                or IsOpportunityOwner().has_object_permission(request, self, application)):
            return Response(
                {'detail': 'Not authorized to view this application.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = self.get_serializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WithdrawApplicationView(views.APIView):
    """Withdraw a pending or reviewed application by the owning student."""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    @extend_schema(
        operation_id='withdraw_application',
        description='Withdraw an application if it has not been accepted or rejected.',
        responses={200: ApplicationDetailSerializer},
    )
    def post(self, request, application_id):
        try:
            application = ApplicationService.get_application(application_id)
        except Application.DoesNotExist:
            return Response(
                {'detail': 'Application not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not IsApplicationOwner().has_object_permission(request, self, application):
            return Response(
                {'detail': 'You can only withdraw your own applications.'},
                status=status.HTTP_403_FORBIDDEN,
            )

        application = ApplicationService.withdraw_application(application)
        serializer = ApplicationDetailSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)
