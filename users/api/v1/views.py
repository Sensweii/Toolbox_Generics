import jwt

from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from .authentication import ActivationPermission
from .authentication import OAuthHandler
from .serializers import UsersSerializer
from .serializers import UserActivationSerializer
from .serializers import UsersListSerializer
from .serializers import UserLoginSerializer
from .serializers import UsersRegistrationSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
        Viewset for handling users endpoint.
    """
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UsersSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        serializer = UsersListSerializer(data=self.queryset, many=True)
        if not serializer.is_valid():
            Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        limited_response = map(lambda x: {
            'id': x['id'],
            'first_name': x['first_name'],
            'detail': x['detail']
        }, serializer.data)
        if request.auth:
            return Response(serializer.data)
        else:
            return Response(limited_response)

    @action(detail=False, methods=['post'])
    def register(self, request):
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
        formatted_token = activation_token.decode('utf-8')
        subject = 'User Registered'
        message = (
            f'To activate account, use the following header when requesting '
            f'at the activation endpoint. Authorization: {formatted_token}')
        sender = settings.EMAIL_HOST_USER

        send_mail(subject, message, sender, [recipient], fail_silently=False)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'],
        permission_classes=[ActivationPermission])
    def activate(self, request, *args, **kwargs):
        serializer = UserActivationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        user.is_activated = True
        user.save()

        # Register app upon activation of user
        OAuthHandler.create_app(user)

        response = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "registration_date": user.created_at,
            "is_activated": user.is_activated
        }
        return Response(
            response,
            status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password'])

        # Generate token for logged in user
        token = OAuthHandler.create_token(user)
        return Response(
            token,
            status=status.HTTP_200_OK)
