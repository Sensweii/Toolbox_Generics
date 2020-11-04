from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Model serializer for UserViewSet."""
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class UsersRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for User Registration."""
    password = serializers.CharField(max_length=128, required=True,
        write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']


class UserActivationSerializer(serializers.ModelSerializer):
    """Serializer for User Activation."""

    class Meta:
        model = User
        fields = ['email']
