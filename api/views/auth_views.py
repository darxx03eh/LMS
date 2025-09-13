from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers.auth_serializers import (
    LoginSerializer,
    LogoutSerializer,
    SignupSerializer,
)


@extend_schema(tags=["auth"])
class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer


class SignupAPIView(APIView):
    serializer_class = SignupSerializer

    @extend_schema(tags=["auth"])
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["auth"])
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
