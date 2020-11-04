import jwt

from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from .serializers import UsersSerializer
from .serializers import UsersRegistrationSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
        Viewset for handling users endpoint.
    """
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UsersSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request, *args, **kwargs):
        serializer = UsersRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        # Save object, manually set password to trigger hashing
        password = serializer.validated_data['password']
        serializer.save()
        user = User.objects.get(email=serializer.data['email'])
        user.set_password(password)
        user.save()

        # Generate activation authorization token and send email
        recipient = serializer.validated_data['email']
        payload = {'recipient': str(recipient)}
        activation_token = jwt.encode(payload, settings.SECRET_KEY)
        subject = 'User Registered'
        message = (
            f'To activate account, use the following header when requesting '
            f'at the activation endpoint. Authorization: {activation_token}')
        sender = settings.EMAIL_HOST_USER

        send_mail(subject, message, sender, [recipient], fail_silently=False)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def activate(self, request, *args, **kwargs):
        pass
