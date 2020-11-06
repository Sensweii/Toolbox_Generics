from django.conf import settings
from django.urls import reverse
from oauth2_provider.models import AccessToken
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer

from users.models import User


class UserSerializer(HyperlinkedModelSerializer):
    """Serializer for User."""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class UserPartialSerializer(UserSerializer):
    """
        Partial serializer for User. Removes `email` and `last_name` for
        unauthenticated access.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name']


class UserCreateSerializer(UserSerializer):
    """Serializer for User create/register."""
    password = serializers.CharField(
        max_length=128, required=True, write_only=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']


class UserLoginSerializer(serializers.Serializer):
    """Email and password serializer for user login."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True,
        write_only=True)

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid/Unregistered email.')
        return email
    
    def validate_password(self, password):
        return password
