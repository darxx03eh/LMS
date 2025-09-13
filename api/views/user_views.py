from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions

from api.serializers.user_serializers import ProfileSerializer, ProfileUpdateSerializer


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
        return self.request.user
