from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from .authentications import OAuthHandler
from .permissions import UserUpdatePermission
from .serializers import UserCreateSerializer
from .serializers import UserLoginSerializer
from .serializers import UserPartialSerializer
from .serializers import UserSerializer
from .utils import EmailSender


class UserViewSet(viewsets.ModelViewSet):
    """
        Viewset for handling users endpoint.
    """
    queryset = User.objects.exclude(is_superuser=True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.action in ['partial_update', 'update']:
            return [UserUpdatePermission()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return UserCreateSerializer
        if self.request.auth:
            return super().get_serializer_class()
        return UserPartialSerializer

    def perform_create(self, serializer):
        user = User.objects.create_user(**serializer.validated_data)
        # Send email with activation token
        recipient = serializer.validated_data['email']
        EmailSender.send_registration_email(recipient)

    def perform_update(self, serializer):
        serializer.save()
        user = self.get_object()
        password = self.request.data.get('password')
        user.update_password(password=password)

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
