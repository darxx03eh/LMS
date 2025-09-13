import os

import cloudinary.uploader
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from drf_spectacular.utils import OpenApiTypes
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    video = serializers.FileField(write_only=True, required=False)
    document = serializers.FileField(write_only=True, required=False)
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), source="course", write_only=True
    )

    class Meta:
        model = Lesson
        fields = (
            "id",
            "course_id",
            "title",
            "description",
            "order",
            "video",
            "document",
            "video_url",
            "document_url",
        )
        read_only_fields = ("id", "video_url", "document_url")

    def get_fields(self):
        fields = super().get_fields()
        fields["video"].swagger_schema_type = OpenApiTypes.BINARY
        fields["document"].swagger_schema_type = OpenApiTypes.BINARY
        return fields

    def _upload_to_cloudinary(self, file, resource_type):
        try:
            result = cloudinary.uploader.upload(file, resource_type=resource_type)
            return result.get("secure_url")
        except Exception as e:
            raise serializers.ValidationError(
                {"file_upload_error": f"Failed to upload {file.name}: {str(e)}"}
            )

    def _upload_to_local(self, file, folder="lessons"):
        path = os.path.join(folder, file.name)
        saved_path = default_storage.save(path, ContentFile(file.read()))
        return default_storage.url(saved_path)

    def create(self, validated_data):
        video = validated_data.pop("video", None)
        document = validated_data.pop("document", None)

        if video:
            # in cloudinary
            # validated_data["video_url"] = self._upload_to_cloudinary(video, "video")
            # in local
            validated_data["video_url"] = self._upload_to_local(video, "lessons/videos")

        if document:
            # in cloudinary
            # validated_data["document_url"] = self._upload_to_cloudinary(document, "raw")
            # in local
            validated_data["document_url"] = self._upload_to_local(
                document, "lessons/docs"
            )

        return Lesson.objects.create(**validated_data)

    def update(self, instance, validated_data):
        video = validated_data.pop("video", None)
        document = validated_data.pop("document", None)

        if video:
            # in cloudinary
            # validated_data["video_url"] = self._upload_to_cloudinary(video, "video")
            # in local
            validated_data["video_url"] = self._upload_to_local(video, "lessons/videos")

        if document:
            # in cloudinary
            # validated_data["document_url"] = self._upload_to_cloudinary(document, "raw")
            # in local
            validated_data["document_url"] = self._upload_to_local(
                document, "lessons/docs"
            )

        return super().update(instance, validated_data)