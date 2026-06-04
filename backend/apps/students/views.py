"""
Student profile views for AttachLink.
Handles student profile use cases, validation, and API responses.
"""

from rest_framework import generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.students.models import StudentProfile
from apps.students.permissions import (
    IsStudentProfileOwner,
    IsStudentProfileVisibleToEmployerOrAdmin,
)
from apps.students.serializers import (
    PublicStudentProfileSerializer,
    StudentProfileSerializer,
)
from apps.students.services import StudentProfileService
from utils.permissions import IsStudent


class StudentProfileView(generics.RetrieveUpdateAPIView):
    """
    Student profile endpoint for the authenticated student.
    GET: retrieve the current student's profile
    PUT/PATCH: update the current student's profile
    """
    queryset = StudentProfile.objects.select_related('user')
    serializer_class = StudentProfileSerializer
    permission_classes = [IsAuthenticated, IsStudent, IsStudentProfileOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return StudentProfileService.get_profile_for_user(self.request.user)

    @extend_schema(
        operation_id='get_student_profile',
        description='Retrieve the profile for the authenticated student.',
        responses=StudentProfileSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id='update_student_profile',
        description='Update the authenticated student profile. Supports partial updates and CV upload.',
        request=StudentProfileSerializer,
        responses=StudentProfileSerializer,
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        profile = StudentProfileService.update_profile(instance, serializer.validated_data)
        output = self.get_serializer(profile)
        return Response(output.data, status=status.HTTP_200_OK)


class StudentProfileDetailView(generics.RetrieveAPIView):
    """
    Public student profile endpoint for employers and admins.
    GET: retrieve a specific student profile by id
    """
    queryset = StudentProfile.objects.select_related('user')
    serializer_class = PublicStudentProfileSerializer
    permission_classes = [IsAuthenticated, IsStudentProfileVisibleToEmployerOrAdmin]
    lookup_field = 'id'
    lookup_url_kwarg = 'student_id'

    @extend_schema(
        operation_id='get_public_student_profile',
        description='Retrieve a public student profile for employers or admins.',
        responses=PublicStudentProfileSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
