from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Course, Enrollment
from api.serializers.course_serializers import (
    CourseSerializer,
    CourseUpdateCreateSerializer,
)
from api.serializers.feedback_serializers import FeedBackSerializer
from api.services.course_services import CourseServices
from utails.custom_permissions import DenyAny, IsAdminUser, IsInstructorUser
from utails.filters import CourseFilter

import logging
logger = logging.getLogger('api.controllers')
@extend_schema(tags=["courses"])
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.prefetch_related(
        "lessons", "instructor", "feedback"
    ).all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated()]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CourseFilter
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.action in ['enroll', 'progress']:
            return None
        if self.request.method in ["POST", "PUT"]:
            return CourseUpdateCreateSerializer
        return CourseSerializer

    def get_permissions(self):
        user = getattr(self.request, "user", None)
        if self.action == "enroll":
            return [permissions.IsAuthenticated()]
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if user and hasattr(user, "role") and user.role.lower() == "admin":
                return [IsAdminUser()]
            elif user and hasattr(user, "role") and user.role.lower() == "instructor":
                return [IsInstructorUser()]
            else:
                return [DenyAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if self.action == "enroll":
            return Course.objects.all()
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if user and hasattr(user, "role") and user.role.lower() == "admin":
                return super().get_queryset()
            elif user and hasattr(user, "role") and user.role.lower() == "instructor":
                return Course.objects.filter(instructor=user)
            return Course.objects.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        user = self.request.user
        if serializer.is_valid():
            logger.info(
                f'{serializer.validated_data} created successfully for user {user.username} has {user.role.lower()} role'
            )
            serializer.save(instructor=self.request.user)
        else: logger.error(f'User: {user.username} field to add course with data {serializer.validated_data}')


    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        course = self.get_object()
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f'User: {user.username} deleted his own {course.title} course successfully')
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to delete {course.title} course')
            raise

    def update(self, request, *args, **kwargs):
        user = self.request.user
        course = self.get_object()
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(
                f'User: {user.username} updated his own {course.title} course successfully with data {request.data}'
            )
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to update {course.title} course')
            raise

    def list(self, request, *args, **kwargs):
        user = self.request.user
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f'Courses retrieved for user {user.username} (id={user.id}) successfully')
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to list courses')
            raise

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {**serializer.data}
        data.update(
            {
                "message": "Course retrieved successfully",
            }
        )
        logger.info(f'Course: {instance.title} retrieved successfully for user {self.request.user}')
        return Response(data)

    @action(detail=True, methods=["get"], url_path="progress")
    def progress(self, request, pk=None):
        course = self.get_object()
        user = self.request.user
        if not course.students.filter(id=user.id).exists():
            logger.warning(f'User: {user.username} not enrolled in {course.title} course')
            raise PermissionDenied("You are not enrolled in this course.")
        course_services = CourseServices()
        prog = course_services.calculate_progress(pk, user)
        logger.info(f'User: {user.username} request to get his progress in {course.title} course')
        return Response(prog)

    @action(detail=True, methods=["get"], url_path="feedback")
    def feedback(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        feedbacks = course.course_feedbacks.all()
        serializer = FeedBackSerializer(feedbacks, many=True)
        if feedbacks.count() <= 0:
            logger.warning(f'No feedback available for {course.title} course')
            return Response(
                {
                    "message": "No feedbacks found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        logger.info(f'feedback available for {course.title} course')
        return Response(
            {
                "result": serializer.data,
                "message": "Feedback retrieved successfully",
            }
        )

    @action(detail=True, methods=['post'], url_path="enroll")
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = self.request.user

        if user.role.lower() != 'student':
            logger.warning(
                f'User: {user.username} has {user.role.lower()} role, only students can enroll'
            )
            raise PermissionDenied("Only students can enroll in courses.")

        if Enrollment.objects.filter(course=course, student=user).exists():
            logger.warning(
                f'User: {user.username} already enrolled in in {course.title} course'
            )
            return Response({
                "message": "You are already enrolled in this course."
            }, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(course=course, student=user)
        logger.info(f'User: {user.username} enrolled in {course.title} course')
        return Response({
            "message": "Enrolled successfully",
        }, status=status.HTTP_200_OK)

