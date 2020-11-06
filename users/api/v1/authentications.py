from django.conf import settings
from django.utils import timezone

from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken
from oauth2_provider.models import Application

from users.models import User


class OAuthHandler:
    """
        Handle OAuth flow methods such as registering app and generating tokens.
    """

    def create_app(user):
        name = f'toolbox_generics_{user.id}'
        Application.objects.create(
            user=user,
            name=name,
            authorization_grant_type='password',
            client_type='public')

    def create_token(user, app=None):
        # Use default toolbox_generics app when not provided
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
