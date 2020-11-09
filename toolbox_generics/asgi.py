import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toolbox_generics.settings.base')

application = get_asgi_application()
