import requests

from django.conf import settings
from django.contrib.auth import authenticate
from django.utils import timezone
from oauth2_provider.models import Application
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class OAuthHandler:
    """
    Handle OAuth flow methods such as registering app and generating tokens.
    """

    def request_token(email, password, app=None):
        # Requests token from authorization server
        if not app:
            app = Application.objects.get(
                name=settings.FIRST_PARTY_APP_NAME)
        url = settings.OAUTH_TOKEN_ENDPOINT
        response = requests.post(
            json={
                'grant_type': 'password',
                'username': email,
                'password': password,
                'client_id': app.client_id,
                'client_secret': app.client_secret
            },
            url=url
        )
        return response.json()

class UserAuthentication:
    """
    Class for handling authentication on User login requests.
    Returns OAuth token.
    """

    def update_last_login(self, user):
        user.last_login = timezone.now()
        user.save()

    def authenticate(self, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(detail='Invalid email.')
        elif not user.is_activated:
            raise AuthenticationFailed(detail='Unactivated account.')

        token = OAuthHandler.request_token(email, password)
        if token.get('access_token'):
            self.update_last_login(user)
        return token
