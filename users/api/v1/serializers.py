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


class UserActivationSerializer(serializers.Serializer):
    """Email serializer for User Activation."""
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid/Unregistered email.')
        if user.is_activated:
            raise serializers.ValidationError('Email already activated.')
        return email


class UserLoginSerializer(serializers.Serializer):
    """Email and password serializer for User Login."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)

    def validate_email(self, email):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid/Unregistered email.')
        return email
    
    def validate_password(self, password):
        return password
