from django.conf import settings
from django.contrib.auth import authenticate as basic_authenticate
from django.utils import timezone

from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class OAuthHandler:
    """
        Handle OAuth flow methods such as registering app and generating tokens.
    """

    def create_app(user):
        name = f'toolbox_generics_{user.id}'
        app = Application.objects.get_or_create(
            user=user,
            name=name,
            authorization_grant_type='password',
            client_type='public')
        return app

    def create_token(user, app=None):
        if not app:
            app = Application.objects.get(
                user=user,
                name=f'toolbox_generics_{user.id}')
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


class UserAuthentication:
    """
        Class for handling basic authentication on User login requests.
    """

    def authenticate(**kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = basic_authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(detail='Invalid credentials.')
        elif not user.is_activated:
            raise AuthenticationFailed(detail='Unactivated account.')

        token = OAuthHandler.create_token(user)
        return token
