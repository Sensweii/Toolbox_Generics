from django.conf import settings
from django.core.mail import send_mail

import jwt


class EmailSender:
    """Class to handle user related notification emails."""

    def send_registration_email(recipient):
        payload = {'recipient': str(recipient)}
        activation_token = jwt.encode(payload, settings.SECRET_KEY)
        formatted_token = activation_token.decode('utf-8')
        subject = 'User Registered'
        message = (
            f'To activate account, POST email to the activate endpoint. '
            f'Provideuse the following header when requesting. '
            f'Authorization: {formatted_token}')
        sender = settings.EMAIL_HOST_USER

        send_mail(subject, message, sender, [recipient], fail_silently=False)
