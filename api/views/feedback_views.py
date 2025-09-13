from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.models import Feedback
from api.serializers.feedback_serializers import ReviewSerializer
from utails.custom_permissions import (
    DenyAny,
    IsAdminUser,
    IsFeedBackOwner,
    IsInstructorUser,
    IsStudentUser,
)


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
        serializer.save(student=self.request.user)
