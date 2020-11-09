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
            'password',
        ]
        extra_kwargs = {
            'url': {'view_name': 'users-detail'},
            'password': {'write_only': True}
        }

