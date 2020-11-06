from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import jwt


class EmailSender:
    """Class to handle user related notification emails."""

    def send_email(self, subject, message, sender, recipient):
        """Generic email sender."""
        html_message = render_to_string(
            'base_email.html',
            {'message': message})
        plain_message = strip_tags(html_message)
        send_mail(
            subject,
            plain_message,
            sender,
            [recipient],
            html_message=html_message,
            fail_silently=False
        )

    def send_registration_email(self, user):
        payload = {'recipient': user.id}
        activation_token = jwt.encode(payload, settings.SECRET_KEY)
        formatted_token = activation_token.decode('utf-8')
        subject = 'User Registered'
        message = (
            f'To activate account, PATCH/UPDATE user field `is_activated`. '
            f'Use the following header when requesting. '
            f'Authorization: {formatted_token}')
        sender = settings.EMAIL_HOST_USER
        self.send_email(subject, message, sender, user.email)
