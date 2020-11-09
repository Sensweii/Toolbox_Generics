from rest_framework import serializers
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(HyperlinkedModelSerializer):
    """Serializer for User."""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'last_login', 'url']
        extra_kwargs = {
            'url': {'view_name': 'users-detail'}
        }


class UserPartialSerializer(UserSerializer):
    """
        Partial serializer for User. Removes `email` and `last_name` for
        unauthenticated access.
    """
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_login', 'url']
        extra_kwargs = {
            'url': {'view_name': 'users-detail'}
        }

class UserCreateSerializer(UserSerializer):
    """Serializer for User create/register."""
    password = serializers.CharField(
        max_length=128, required=True, write_only=True)
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'is_activated',
            'url',
            'password'
        ]
        extra_kwargs = {
            'url': {'view_name': 'users-detail'}
        }
