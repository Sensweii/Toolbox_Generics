from django.conf import settings
from django.utils import timezone

import jwt
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from users.models import User


class OAuthHandler:
    """
        Handle OAuth flow methods such as registering app and generating tokens.
    """

    def create_app(user):
        name = f'user_api_{user.id}'
        Application.objects.create(
            user=user,
            name=name,
            authorization_grant_type='password',
            client_type='public')

    def create_token(user, app=None):
        # Use default user_api app when not provided
        if not app:
            app = Application.objects.get(
                user=user,
                name=f'user_api_{user.id}')
        time_to_live = settings.OAUTH_TOKEN_TTL
        expiration_time = (
            timezone.now() + timezone.timedelta(seconds=time_to_live))
        oauth_token = AccessToken.objects.create(
            user=user,
            application=app,
            expires=expiration_time,
            token=generate_token()
        )
        response_token = {
            'access_token': oauth_token.token,
            'token_type': 'Bearer',
            'expires_on': expiration_time
        }
        return response_token


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
        try:
            decoded_token = jwt.decode(
                bytes(token, 'utf-8'), settings.SECRET_KEY)
        except jwt.exceptions.InvalidSignatureError:
            raise PermissionDenied(detail='Token signature mismatch.')
        except TypeError:
            raise PermissionDenied('Invalid token.')
        if decoded_token['recipient'] != user_email:
            raise PermissionDenied('Email token mismatch.')
        return True

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
        else:
            permission_granted = self.verify_oauth_token(request, obj)        
        return permission_granted
