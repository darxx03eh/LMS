from datetime import datetime

from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from api.models.user import User


class LoginSerializer(TokenObtainPairSerializer):
    username_or_email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)

    def validate(self, attrs):
        username_or_email = attrs.get("username_or_email")
        password = attrs.get("password")
        try:
            user = User.objects.get(username=username_or_email)
        except User.DoesNotExist:
            try:
                user = User.objects.get(email=username_or_email)
            except User.DoesNotExist:
                raise serializers.ValidationError(
                    "No active account found with the given credentials"
                )

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect username or password")

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        user.last_login = datetime.now()
        user.save(update_fields=["last_login"])
        return {
            "username": user.username,
            "role": user.role,
            "access": str(access),
            "refresh": str(refresh),
            "message": "Data verified and login successful",
        }


class SignupSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = BaseUserCreateSerializer.Meta.fields + (
            "first_name",
            "last_name",
            "phone_number",
            "role",
            "username",
        )

    def validate_phone_number(self, value):
        if len(value) == 13:
            if value.startswith("+970") or value.startswith("+972"):
                return value
        raise serializers.ValidationError(
            "Phone number must be entered in the format: +970 or +972 and has 13 characters with +"
        )

    def validate_role(self, value: str):
        if value.lower() in ["student", "instructor"]:
            return value
        raise serializers.ValidationError(
            'Role must be either "student" or "instructor"'
        )

    def validate_username(self, value):
        if len(value) >= 3 and len(value) <= 20:
            return value
        raise serializers.ValidationError(
            "Username must be between 3 and 20 characters"
        )

    def validate_first_name(self, value):
        if len(value) >= 2 and len(value) < 50:
            return value
        raise serializers.ValidationError(
            "First name must be between 2 and 50 characters"
        )

    def validate_last_name(self, value):
        if len(value) >= 2 and len(value) < 50:
            return value
        raise serializers.ValidationError(
            "Last name must be between 2 and 50 characters"
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["message"] = f"An {instance.role} account has been created"
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            self.token = RefreshToken(value)
        except:
            raise serializers.ValidationError("Invalid or expired token")
        return value

    def save(self, **kwargs):
        self.token.blacklist()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["message"] = "User logged out"
        return data
