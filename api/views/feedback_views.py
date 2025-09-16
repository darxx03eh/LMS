from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.models import Feedback, Course
from api.serializers.feedback_serializers import ReviewSerializer
from utails.custom_permissions import (
    DenyAny,
    IsAdminUser,
    IsFeedBackOwner,
    IsInstructorUser,
    IsStudentUser,
)

import logging
logger = logging.getLogger('api.controllers')
@extend_schema(tags=["Feedbacks"])
class FeedbackViewSet(ModelViewSet):
    queryset = Feedback.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_permissions(self):
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return [DenyAny()]
        if self.request.method == "POST":
            return [IsStudentUser()]
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            if user and hasattr(user, "role") and user.role.lower() == "admin":
                return [IsAdminUser()]
            elif user and hasattr(user, "role") and user.role.lower() == "instructor":
                return [IsInstructorUser()]
            else:
                return [IsFeedBackOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = getattr(self.request, "user", None)
        if not user or not user.is_authenticated:
            return Feedback.objects.none()
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            if user and hasattr(user, "role") and user.role.lower() == "admin":
                return super().get_queryset()
            elif user and hasattr(user, "role") and user.role.lower() == "instructor":
                return Feedback.objects.filter(course__instructor=user)
            else:
                return Feedback.objects.filter(student=user)
        return super().get_queryset()

    def perform_create(self, serializer):
        user = self.request.user
        course = Course.objects.get(pk=serializer.validated_data['course_id'])
        if serializer.is_valid():
            serializer.save(student=user)
            logger.info(f'User: {user.username} add feedback to {course.title} course with data {serializer.validated_data}')

        else: logger.error(f'User: {user.username} field to add feedback to {course.title} course')

    def destroy(self, request, *args, **kwargs):
        user = self.request.user
        feedback = get_object_or_404(Feedback, pk=self.kwargs["pk"])
        try:
            response = super().destroy(request, *args, **kwargs)
            logger.info(f'User: {user.username} remove feedback from {feedback.course.title} course')
            return response
        except Exception as e:
            logger.error(
                f'User: {user.username} field to remove feedback from {feedback.course.title} course with error {str(e)}'
            )
            raise

    def list(self, request, *args, **kwargs):
        user = self.request.user
        try:
            response = super().list(request, *args, **kwargs)
            logger.info(f'Feedbacks retrieved for user {user.username} (id={user.id}) successfully')
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to list feedbacks')
            raise

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = {**serializer.data}
        data.update(
            {
                "message": "Feedback retrieved successfully",
            }
        )
        logger.info(f'Feedback: (id={instance.id}) retrieved successfully for user {self.request.user}')
        return Response(data)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        feedback = self.get_object()
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(
                f'User: {user.username} updated his own feedback (id={feedback.id}) successfully with data {request.data}'
            )
            return response
        except Exception as e:
            logger.error(f'User: {user.username} failed to update (id={feedback.id}) feedback')
            raise
