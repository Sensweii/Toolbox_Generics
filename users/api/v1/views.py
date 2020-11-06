from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from .authentication import ActivationPermission
from .authentication import ResourceUpdatePermission
from .authentication import OAuthHandler
from .serializers import UserSerializer
from .serializers import UserActivationSerializer
from .serializers import UserListSerializer
from .serializers import UserLoginSerializer
from .serializers import UserPasswordSerializer
from .serializers import UserRegistrationSerializer
from .utils import EmailSender


class UserViewSet(viewsets.ModelViewSet):
    """
        Viewset for handling users endpoint.
    """
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        response = {
            'id': instance.id,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'list': settings.API_USERS_URL,
            'change_password': (
                f'{settings.API_USERS_URL}{instance.id}/change_password')
        }
        if request.auth:
            return Response(response)
        limited_response = dict([
            (k,v) for k,v in response.items()
            if k in ['id', 'first_name', 'list']])
        return Response(limited_response)

    def list(self, request):
        serializer = UserListSerializer(data=self.queryset, many=True)
        _ = serializer.is_valid()
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
        serializer = UserRegistrationSerializer(data=request.data)
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
        EmailSender.send_registration_email(recipient)
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
        if not user:
            return Response(
            {'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED)

        # Generate token for logged in user
        token = OAuthHandler.create_token(user)
        return Response(
            token,
            status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'],
        permission_classes=[ResourceUpdatePermission])
    def change_password(self, request, *args, **kwargs):
        token = request.headers.get('Authorization').replace('Bearer ', '')
        request.data.update({'token': token, 'pk': kwargs.get('pk')})
        serializer = UserPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        response = serializer.validated_data
        return Response(
            response,
            status=status.HTTP_200_OK)
