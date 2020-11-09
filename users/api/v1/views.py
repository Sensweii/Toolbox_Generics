from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from users.models import User
from .permissions import UserUpdatePermission
from .serializers import UserCreateUpdateSerializer
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
        if self.action in ['partial_update', 'update', 'destroy']:
            return [UserUpdatePermission()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update', 'update']:
            return UserCreateUpdateSerializer
        if self.request.auth:
            return super().get_serializer_class()
        return UserPartialSerializer

    def perform_create(self, serializer):
        serializer.save()
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        password = self.request.data.get('password')
        user.update_password(password)
        # Send email with activation token
        EmailSender().send_registration_email(user)

    def perform_update(self, serializer):
        serializer.save()
        user = self.get_object()
        password = self.request.data.get('password')
        user.update_password(password=password)
