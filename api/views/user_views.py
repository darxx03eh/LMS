from Scripts.bottle import response
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from api.serializers.user_serializers import ProfileSerializer, ProfileUpdateSerializer

import logging
logger = logging.getLogger('api.controllers')
@extend_schema(tags=["users"])
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ["get", "patch"]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ProfileUpdateSerializer
        return ProfileSerializer

    def get_object(self):
        user = self.request.user
        logger.info(f'Profile retrieved for user {user.username} (id={user.id})')
        return user

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        logger.info(f'Profile update requested by user {user.username} (id={user.id}) with data: {request.data}')
        try:
            response = super().patch(request, *args, **kwargs)
            logger.info(f'Profile updated successfully for user {user.username} (id={user.id})')
            return response
        except Exception as e:
            logger.error(f'Failed update profile for user={user.username}. Error: {str(e)}')
            raise

