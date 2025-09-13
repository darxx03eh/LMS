from django.db import models

from .course import Course
from .user import User


class Lesson(models.Model):
    id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    students = models.ManyToManyField(
        User, through="CompletedLesson", related_name="completed_lessons_courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField()
    video_url = models.URLField(max_length=255, null=True, blank=True)
    document_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
