from rest_framework import serializers


class LoginViewSerializer(serializers.Serializer):
    """Serializer class for login requests."""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=128, required=True)
