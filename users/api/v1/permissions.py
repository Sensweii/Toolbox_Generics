import jwt

from django.conf import settings
from django.utils import timezone

from oauth2_provider.models import AccessToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class UserUpdatePermission(BasePermission):
    """
    Permission class for handling PATCH requests to a user resource.
    """

    def verify_oauth_token(self, request, obj):
        token = request.headers.get('Authorization')
        if not token:
            raise PermissionDenied(detail='Restricted access.')
        try:
            formatted_token = token.replace('Bearer ', '')
            AccessToken.objects.get(
                user=obj,
                token=formatted_token,
                expires__gt=timezone.now())
        except AccessToken.DoesNotExist:
            raise PermissionDenied(detail='Invalid token.')
        return True

    def has_object_permission(self, request, view, obj):
        return self.verify_oauth_token(request, obj)


class UserActivatePermission(BasePermission):
    """
    Permission class for handling PATCH requests to user's is_activated field.
    """

    def verify_activation_token(self, request, obj):
        token = request.headers.get('Authorization')
        user_id = obj.id
        try:
            decoded_token = jwt.decode(
                bytes(token, 'utf-8'), settings.SECRET_KEY)
        except jwt.exceptions.InvalidSignatureError:
            raise PermissionDenied(detail='Token signature mismatch.')
        except jwt.exceptions.DecodeError:
            raise PermissionDenied(detail='Invalid token.')
        except TypeError:
            raise PermissionDenied('Invalid token.')
        if decoded_token['recipient'] != user_id:
            raise PermissionDenied('User token mismatch.')
        else:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.verify_activation_token(request, obj)
