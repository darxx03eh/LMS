from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Feedback


class ReviewSerializer(ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Feedback
        fields = ("id", "student", "rate", "comment", "created_at", "course_id")
        read_only_fields = ("id", "student", "created_at")

    def create(self, validated_data):
        validated_data["student"] = self.context["request"].user
        course_id = validated_data.pop("course_id")
        validated_data["course_id"] = course_id
        return super().create(validated_data)

    def validate(self, data):
        user = self.context["request"].user
        course_id = data.get("course_id")

        if self.instance is None:
            if Feedback.objects.filter(
                student_id=user.id, course_id=course_id
            ).exists():
                raise serializers.ValidationError(
                    {"review": "You have already reviewed this course."}
                )
        return data


class FeedBackSerializer(ModelSerializer):
    student = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = Feedback
        fields = ("id", "rate", "comment", "created_at", "student")
