import json

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters

from oauth2_provider.views import TokenView as BaseTokenView
from rest_framework.exceptions import AuthenticationFailed


class TokenView(BaseTokenView):
    """
    Inherits oauth package TokenView. Performs additional check on user's
    `is_activated` field.
    """

    def update_last_login(self, user):
        user.last_login = timezone.now()
        user.save()

    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('username')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed(detail='Invalid email.')
        elif not user.is_activated:
            raise AuthenticationFailed(detail='Unactivated account.')
        self.update_last_login(user)
        return super().post(request, *args, *kwargs)
