from django.contrib import admin
from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

from .views.auth_views import LoginAPIView, LogoutAPIView, SignupAPIView
from .views.course_views import CourseViewSet
from .views.feedback_views import FeedbackViewSet
from .views.lessons_views import LessonViewSet
from .views.user_views import ProfileAPIView

root = "api"
version = "v1"
rule = f"{root}/{version}"

AUTH = [
    path(f"{rule}/login", LoginAPIView.as_view(), name="login"),
    path(f"{rule}/signup", SignupAPIView.as_view(), name="signup"),
    path(f"{rule}/logout", LogoutAPIView.as_view(), name="logout"),
]

USER = [
    path(f"{rule}/users", ProfileAPIView.as_view(), name="profile"),
]
COURSE = [
    path(
        f"{rule}/courses",
        CourseViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="courses",
    ),
    path(
        f"{rule}/courses/<int:pk>",
        CourseViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "put": "update",
            }
        ),
    ),
    path(
        f"{rule}/courses/<int:pk>/progress", CourseViewSet.as_view({"get": "progress"})
    ),
    path(
        f"{rule}/courses/<int:pk>/feedbacks", CourseViewSet.as_view({"get": "feedback"})
    ),
    path(
        f'{rule}/courses/<int:pk>/enroll', CourseViewSet.as_view({"post": "enroll"})
    ),
]

LESSON = [
    path(
        f"{rule}/lessons",
        LessonViewSet.as_view(
            {
                "get": "list",
                "post": "create",
            }
        ),
        name="lessons",
    ),
    path(
        f"{rule}/lessons/<int:pk>",
        LessonViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "put": "update",
            }
        ),
    ),
    path(
        f"{rule}/course/<int:pk>/lessons",
        LessonViewSet.as_view({"get": "course_lessons"}),
    ),
    path(
        f"{rule}/lessons/<int:pk>/mark_completed",
        LessonViewSet.as_view({"post": "mark_completed"}),
    ),
]
FEEDBACK = [
    path(
        f"{rule}/feedbacks",
        FeedbackViewSet.as_view(
            {
                "get": "list",
            }
        ),
    ),
    path(
        f"{rule}/courses/feedback",
        FeedbackViewSet.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        f"{rule}/feedbacks/<int:pk>",
        FeedbackViewSet.as_view(
            {
                "get": "retrieve",
                "delete": "destroy",
                "put": "update",
            }
        ),
    ),
]
urlpatterns = [*AUTH, *USER, *COURSE, *LESSON, *FEEDBACK]