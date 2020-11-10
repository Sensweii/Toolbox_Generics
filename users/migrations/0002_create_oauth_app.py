from django.conf import settings
from django.db import migrations


def create_users_api_oauth_app(apps, schema_editor):
    Application = apps.get_model('oauth2_provider', 'Application')
    Application.objects.create(
        name=settings.FIRST_PARTY_APP_NAME,
        client_type='confidential',
        authorization_grant_type='password'
    )


def reverse_create_users_api_oauth_app(apps, schema_editor):
    Application = apps.get_model('oauth2_provider', 'Application')
    app = Application.objects.get(
        name=settings.FIRST_PARTY_APP_NAME,
        client_type='confidential',
        authorization_grant_type='password'
    )
    app.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            create_users_api_oauth_app,
            reverse_create_users_api_oauth_app,
        )
    ]
