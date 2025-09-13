from django.db import models

from .course import Course
from .user import User


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_enrollments"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_enrollments"
    )
    enroll_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student")

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"
