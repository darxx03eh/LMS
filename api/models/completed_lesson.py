from django.db import models

from .lesson import Lesson
from .user import User


class CompletedLesson(models.Model):
    id = models.AutoField(primary_key=True)
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="completed_lessons"
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="completed_lessons"
    )
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student.username} completed {self.lesson.title} on {self.completed_at}"
