from django.contrib.auth import get_user_model
from rest_framework import generics, mixins, permissions
from rest_framework.authtoken.views import ObtainAuthToken

from . import serializers


class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = serializers.CustomAuthTokenSerializer


class UserCarsApiView(generics.ListAPIView):
    serializer_class = serializers.CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.car.all().order_by('id')


class AllUsersApiView(mixins.UpdateModelMixin, generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_user_model().objects.all().order_by('id')


class MeApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class SignUpApiView(generics.CreateAPIView):
    serializer_class = serializers.SignUpSerializer
