from django.conf import settings
from django.urls import reverse
from oauth2_provider.models import AccessToken
from rest_framework import serializers

from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Model serializer for UserViewSet."""

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']


class UsersListSerializer(UsersSerializer):
    """Add ID and Details link to model serializer."""
    detail = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'detail']

    def get_detail(self, obj):
        return settings.API_USERS_URL + str(obj.id)


class UsersRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(max_length=128, required=True,
        write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password']


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


class UserPasswordSerializer(serializers.Serializer):
    """Password serializer for user password change."""
    password = serializers.CharField(max_length=128, required=True,
        write_only=True)
    pk = serializers.IntegerField(required=True)
    token = serializers.CharField(max_length=128, required=True,
        write_only=True)

    def validate_password(self, password):
        return password

    def validate_pk(self, pk):
        return int(pk)

    def validate_token(self, token):
        return token

    def validate(self, data):
        pk = data.get('pk')
        password = data.get('password')
        token = data.get('token')
        user = User.objects.get(id=pk)
        try:
            access_token = AccessToken.objects.get(user=user, token=token)
        except AccessToken.DoesNotExist:
            raise serializers.ValidationError(
                'Unathorized action.')
        user.set_password(password)
        user.save()
        validated_data = user.__dict__
        return dict([(k,v) for k,v in validated_data.items()
            if k in ['id', 'email', 'first_name', 'last_name']])
