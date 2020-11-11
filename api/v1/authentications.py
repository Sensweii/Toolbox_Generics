import requests

from django.conf import settings

from oauth2_provider.models import Application


class OAuthHandler:
    """
    Handle OAuth flow methods such as registering app and generating tokens.
    """

    def request_token(self, email, password, app=None):
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

    def authenticate(self, **kwargs):
        """
        First party app requests token from authorization server.
        """
        email = kwargs.get('email')
        password = kwargs.get('password')
        token = OAuthHandler().request_token(email, password)
        return token
