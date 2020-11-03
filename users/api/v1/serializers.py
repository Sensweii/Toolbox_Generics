from rest_framework import serializers

from users.models import User


class UsersViewSetSerializer(serializers.ModelSerializer):
    """Model serializer for UserViewSet."""
    class Meta:
        model = User
        fields = ['email_address', 'first_name', 'last_name']
