from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Course, Lesson
from api.serializers.lessons_serializers import LessonSerializer
from utails.custom_permissions import IsCourseOwner


@extend_schema(tags=["lessons"])
class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "mark_completed":
            return [IsAuthenticated()]
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated(), IsCourseOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "mark_completed":
            return None
        return super().get_serializer_class()

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if self.request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            if user and hasattr(user, "role") and user.role.lower() == "admin":
                return super().get_queryset()
            elif user and hasattr(user, "role") and user.role.lower() == "instructor":
                return Lesson.objects.filter(course__instructor=user)

        if user and hasattr(user, "role") and user.role.lower() == "student":
            return Lesson.objects.filter(course__course_enrollments__student=user)
        elif user and hasattr(user, "role") and user.role.lower() == "instructor":
            return Lesson.objects.filter(course__instructor=user)
        return Lesson.objects.all()

    def perform_create(self, serializer):
        course = serializer.validated_data["course"]

        if self.request.user.role.lower() == "instructor":
            if course.instructor != self.request.user:
                raise PermissionDenied("You can only add lessons to your own courses.")

        serializer.save(course=course)

    @action(detail=True, methods=["get"], url_path="course_lessons")
    def course_lessons(self, request, pk=None):
        lessons = self.get_queryset().filter(course__id=pk)
        print(lessons)
        serializer = LessonSerializer(lessons, many=True)
        if not lessons:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="mark_completed")
    def mark_completed(self, request, pk=None):
        lesson = self.get_object()
        user = request.user

        if not lesson.course.students.filter(id=user.id).exists():
            raise PermissionDenied("You are not enrolled in this course.")

        if lesson.students.filter(id=user.id).exists():
            raise PermissionDenied("You are already enrolled in this course.")

        lesson.students.add(user)
        return Response(
            {
                "message": f"Lesson {lesson.title} marked as completed",
            },
            status.HTTP_200_OK,
        )
