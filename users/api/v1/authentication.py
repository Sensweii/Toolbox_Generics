from django.conf import settings
from django.utils import timezone

import jwt
from oauthlib.common import generate_token
from oauth2_provider.models import Application
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class ActivationPermission(BaseAuthentication):
    """
        Handles token verification for users activating their emails.
    """

    def has_permission(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        user_email = request.data['email']
        try:
            decoded_token = jwt.decode(
                bytes(token, 'utf-8'), settings.SECRET_KEY)
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Token signature mismatch.')
        except TypeError:
            raise AuthenticationFailed('Invalid token.')
        if decoded_token['recipient'] != user_email:
            raise AuthenticationFailed('Email token mismatch.')
        return True


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

    def create_token(user, app):
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
