from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template

import jwt

from django.core.mail import send_mail
from django.template.loader import render_to_string


class Email:
    """Base class to handle notification emails."""

    subject = ''
    text_template = ''
    html_template = ''
    recipients = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_subject(self):
        if not self.subject:
            raise Exception('Inheriting class must set `subject`.')
        return self.subject

    def get_text_template_name(self):
        if not self.text_template:
            raise Exception('Inheriting class must set `text_template`.')
        return self.text_template

    def get_html_template_name(self):
        if not self.html_template:
            raise Exception('Inheriting class must set `template`.')
        return self.html_template

    def get_recipients(self):
        return self.recipients

    def get_context(self, **kwargs):
        return kwargs

    def send(self):
        context = self.get_context()
        subject = self.get_subject()
        text_template = self.get_text_template_name()
        html_template = self.get_html_template_name()
        text_content = render_to_string(text_template, context)
        html_content = render_to_string(html_template, context)
        recipients = self.get_recipients()

        send_mail(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            recipients,
            html_message=html_content,
            fail_silently=False)


class RegistrationEmail(Email):
    """Class for handling registration emails."""

    subject = 'User Registered'
    text_template = '../templates/registration.txt'
    html_template = '../templates/registration.html'

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.recipients = [user.email]

    def generate_token(self):
        data = {'recipient': self.user.id}
        activation_token = jwt.encode(data, settings.SECRET_KEY)
        return activation_token.decode('utf-8')
    
    def get_context(self):
        return {
            'token': self.generate_token(),
            'link': f'{settings.API_USERS_URL}{self.user.id}/status/'
        }
