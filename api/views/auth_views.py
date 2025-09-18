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
import logging
def sum():
    pass

# this is to test conflict
logger = logging.getLogger('api.controllers')
@extend_schema(tags=["auth"])
class LoginAPIView(TokenObtainPairView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        username_or_email = request.data.get('username_or_email')

        try:
            response = super().post(request, *args, **kwargs)
            logger.info(f'User: {username_or_email} logged in successfully')
            return response
        except Exception as e:
            logger.error(f'Failed login attempt for user={username_or_email}. Error: {str(e)}')
            raise

def sum():
    pass

# this is to test conflict

class SignupAPIView(APIView):
    serializer_class = SignupSerializer
    @extend_schema(tags=["auth"])
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f'User: {user.username} signed up successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning(f'Signup failed with errors: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(tags=["auth"])
    def post(self, request): # logged out successfully
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'User: {request.user.username} logged out successfully')
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            logger.error(f'Logout failed with errors: {serializer.errors}')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
