from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Course, Lesson
from api.serializers.lessons_serializers import LessonSerializer
from utails.custom_permissions import IsCourseOwner

import logging
logger = logging.getLogger('api.controllers')
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
        user = self.request.user
        if user.role.lower() == "instructor":
            if course.instructor != user:
                logger.warning(
                    f'Instructor {user.username} tried to add lessons to {course.title} course, and this course not for him'
                )
                raise PermissionDenied("You can only add lessons to your own courses.")

        if serializer.is_valid():
            logger.info(f'Instructor: {user.username} added lessons to {course.title} course with data {serializer.data}')
            serializer.save(course=course)
        else: logger.error(f'Instructor: {user.username} field to add lessons to {course.title} course with data {serializer.data}')

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f'User: {user.username} removed lesson from {lesson.course.title} course successfully')
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to remove lesson from {lesson.course.title} course with error {e}')
            raise

    def update(self, request, *args, **kwargs):
        user = self.request.user
        lesson = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(
                f'User: {user.username} updated {lesson.title} lesson successfully with data {request.data}'
            )
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to update {lesson.title} lesson')
            raise

    def list(self, request, *args, **kwargs):
        user = self.request.user
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f'Lessons retrieved for user {user.username} (id={user.id}) successfully')
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to list Lessons')
            raise


    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(Lesson, pk=self.kwargs["pk"])
        serializer = self.get_serializer(instance)
        data = {**serializer.data}
        data.update(
            {
                "message": "Lesson retrieved successfully",
            }
        )
        logger.info(f'Lesson: {instance.title} retrieved successfully for user {self.request.user}')
        return Response(data)


    @action(detail=True, methods=["get"], url_path="course_lessons")
    def course_lessons(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        lessons = self.get_queryset().filter(course__id=pk)
        serializer = LessonSerializer(lessons, many=True)
        if not lessons:
            logger.warning(f'no lessons found for user {self.request.user.username} in {course.title} course')
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        logger.info(f'lessons found for user {self.request.user.username} in {course.title} course')
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="mark_completed")
    def mark_completed(self, request, pk=None):
        lesson = self.get_object()
        user = request.user

        if not lesson.course.students.filter(id=user.id).exists():
            logger.warning(f'User: {user.username} not enrolled in {lesson.course.title} course')
            raise PermissionDenied("You are not enrolled in this course.")

        lesson.students.add(user)
        logger.info(
            f'Lesson: {lesson.title} in {lesson.course.title} course mark completed for user {user.username} successfully'
        )
        return Response(
            {
                "message": f"Lesson {lesson.title} marked as completed",
            },
            status.HTTP_200_OK,
        )
