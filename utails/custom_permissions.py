from rest_framework import permissions

from api.models import Course


class IsStudentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == "student"


class IsInstructorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role.lower() == "instructor"
        )


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.lower() == "admin"


class DenyAny(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class IsCourseOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            course_id = request.data.get("course_id")
            try:
                if course_id:
                    course = Course.objects.get(id=course_id)
                    return course.instructor == request.user
            except Course.DoesNotExist:
                return False
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.role.lower() == "admin":
            return True
        return obj.course.instructor == request.user


class IsFeedBackOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if (
            obj.student == user
            or user.role.lower() == "admin"
            or (obj.course.instructor == user and user.role.lower() == "instructor")
        ):
            return True
        return False
