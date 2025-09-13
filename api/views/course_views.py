from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Course
from api.serializers.course_serializers import (
    CourseSerializer,
    CourseUpdateCreateSerializer,
)
from api.serializers.feedback_serializers import FeedBackSerializer
from api.services.course_services import CourseServices
from utails.custom_permissions import DenyAny, IsAdminUser, IsInstructorUser
from utails.filters import CourseFilter


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
        if self.action == "progress":
            return None
        if self.request.method in ["POST", "PUT"]:
            return CourseUpdateCreateSerializer
        return CourseSerializer

    def get_permissions(self):
        user = getattr(self.request, "user", None)
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
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if user and hasattr(user, "role") and user.role.lower() == "admin":
                return super().get_queryset()
            elif user and hasattr(user, "role") and user.role.lower() == "instructor":
                return Course.objects.filter(instructor=user)
            return Course.objects.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {**serializer.data}
        data.update(
            {
                "message": "Course retrieved successfully",
            }
        )
        return Response(data)

    @action(detail=True, methods=["get"], url_path="progress")
    def progress(self, request, pk=None):
        course = self.get_object()
        user = self.request.user
        if not course.students.filter(id=user.id).exists():
            raise PermissionDenied("You are not enrolled in this course.")
        course_services = CourseServices()
        prog = course_services.calculate_progress(pk, user)
        return Response(prog)

    @action(detail=True, methods=["get"], url_path="feedback")
    def feedback(self, request, pk=None):
        course = Course.objects.get(pk=pk)
        feedbacks = course.course_feedbacks.all()
        serializer = FeedBackSerializer(feedbacks, many=True)
        if feedbacks.count() <= 0:
            return Response(
                {
                    "message": "No feedbacks found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {
                "result": serializer.data,
                "message": "Feedback retrieved successfully",
            }
        )
