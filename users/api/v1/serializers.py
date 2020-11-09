from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(HyperlinkedModelSerializer):
    """Serializer for authenticated User."""
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'last_login',
            'url',
        ]
        extra_kwargs = {
            'url': {'view_name': 'users-detail'}
        }


class UserPartialSerializer(UserSerializer):
    """
    Partial serializer for unauthenticated User. Removes `email`, `last_name`,
    and `last_login`.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'url',
        ]
        extra_kwargs = {
            'url': {'view_name': 'users-detail'}
        }


class UserCreateUpdateSerializer(UserSerializer):
    """Serializer for User create/register."""
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'url',
            'is_activated',
            'password',
        ]
        extra_kwargs = {
            'url': {'view_name': 'users-detail'},
            'is_activated': {'read_only': True},
            'password': {'write_only': True}
        }


class UserActivateSerializer(UserSerializer):
    """Serializer for User activation."""
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_activated',
            'url',
        ]
        extra_kwargs = {
            'url': {'view_name': 'users-detail'},
        }

    def validate_is_activated(self, is_activated):
        if is_activated:
            return is_activated
        raise serializers.ValidationError('Action not allowed.')
