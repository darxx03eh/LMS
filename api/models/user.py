from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = (
            "student",
            "Student",
        )
        INSTRUCTOR = "instructor", "Instructor"
        ADMIN = "admin", "Admin"

    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)

    def __str__(self):
        return self.username
