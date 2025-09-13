from django.db import models

from .course import Course
from .time_stamped_mix_in import TimeStampedMixin
from .user import User


class Feedback(TimeStampedMixin, models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_feedbacks"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="course_feedbacks"
    )
    comment = models.TextField()
    rate = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        return f"Feedback by: {self.student.username} on {self.course.title}"