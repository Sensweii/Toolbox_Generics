from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from users.models import User
from .permissions import UserUpdatePermission
from .serializers import UserCreateSerializer
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
