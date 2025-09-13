from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Course, User


class ProfileSerializer(ModelSerializer):
    enrolled_courses_count = serializers.SerializerMethodField()
    courses_created_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "date_joined",
            "enrolled_courses_count",
            "courses_created_count",
        )
        read_only_fields = ("id", "role", "date_joined")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.instance if isinstance(self.instance, User) else None
        if user:
            if user.role.lower() in ["student", "admin"]:
                self.fields.pop("courses_created_count")
            if user.role.lower() in ["instructor", "admin"]:
                self.fields.pop("enrolled_courses_count")

    def get_enrolled_courses_count(self, obj):
        return Course.objects.filter(students=obj).count()

    def get_courses_created_count(self, obj):
        return Course.objects.filter(user=obj).count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["message"] = "User retrieve successfully"
        return data


class ProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone_number")

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["message"] = "User update successfully"
        return data
