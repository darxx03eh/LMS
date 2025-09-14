from django.db import transaction
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Course, Enrollment, Feedback, Lesson, User


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ("title", "description", "order")


class InstructorSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email", "phone_number")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context.get("request").user if self.context.get("request") else None
        if user and user.role.lower() == "student":
            data.pop("email", None)
        return data


class StudentSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class FeedBacksSerializer(ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ("id", "student", "rate", "comment")


class CourseSerializer(ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    # feedback = FeedBacksSerializer(source='course_feedbacks',many=True, read_only=True)
    students_enrolled_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            "id",
            "title",
            "description",
            "category",
            "level",
            "instructor",
            "created_at",
            "updated_at",
            "average_rating",
            "students_enrolled_count",
        )

    def get_students_enrolled_count(self, obj):
        return Enrollment.objects.filter(course=obj).count()


class CourseUpdateCreateSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, required=False)
    instructor = InstructorSerializer(read_only=True)
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Course
        fields = ("id", "title", "description", "category", "level", "lessons", "instructor")

    def create(self, validated_data):
        lessons = validated_data.pop("lessons")
        with transaction.atomic():
            course = Course.objects.create(**validated_data)
            for lesson in lessons:
                Lesson.objects.create(course=course, **lesson)
        return course

    def update(self, instance, validated_data):
        lessons = validated_data.pop("lessons", None)
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if lessons is not None:
                instance.lessons.all().delete()
                for lesson in lessons:
                    Lesson.objects.create(course=instance, **lesson)
        return instance
