from django.db import models
from django.db.models import Avg

from .time_stamped_mix_in import TimeStampedMixin
from .user import User


class Course(TimeStampedMixin, models.Model):
    class Levels(models.TextChoices):
        BEGINNER = "beginner"
        INTERMEDIATE = "intermediate"
        ADVANCED = "advanced"

    id = models.AutoField(primary_key=True)
    instructor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="created_courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    level = models.CharField(
        max_length=15, choices=Levels.choices, default=Levels.BEGINNER
    )
    students = models.ManyToManyField(
        User, through="Enrollment", related_name="enrolled_courses"
    )
    feedback = models.ManyToManyField(
        User, through="Feedback", related_name="feedback_courses"
    )

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        return self.course_feedbacks.aggregate(avg=Avg("rate"))["avg"] or 0