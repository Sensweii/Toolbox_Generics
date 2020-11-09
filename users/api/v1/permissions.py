from django.conf import settings
from django.utils import timezone

import jwt
from oauth2_provider.models import AccessToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from users.models import User


class UserUpdatePermission(BasePermission):
    """
        Custom permission for handling PATCH requests to a user resource.
        There are two cases to handle:
            1. Updating `is_activated` field (Activation) will require a
                json webtoken (activation code sent by email).
            2. Updating user's info (e.g. email, name, password, etc.) will
                require login (oauth token authorization).
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

    def verify_oauth_token(self, request, obj):
        token = request.headers.get('Authorization')
        if not token:
            raise PermissionDenied(detail='Restricted access.')
        try:
            formatted_token = token.replace('Bearer ', '')
            access = AccessToken.objects.get(
                user=obj,
                token=formatted_token,
                expires__gt=timezone.now())
        except AccessToken.DoesNotExist:
            raise PermissionDenied(detail='Invalid token.')
        return True


    def has_object_permission(self, request, view, obj):
        # Check if request is activation or info update
        activation_request = request.data.get('is_activated')
        if activation_request:
            permission_granted = self.verify_activation_token(request, obj)
        elif type(activation_request) == bool:
            raise PermissionDenied(detail=f'Reversing activation not allowed. '
                f'Delete the account instead.')
            permission_granted = False
        else:
            permission_granted = self.verify_oauth_token(request, obj)        
        return permission_granted
