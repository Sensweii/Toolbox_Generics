from rest_framework import viewsets

from .serializers import UsersViewSetSerializer


class UsersViewSet(viewsets.ModelViewSet):
    """
        Viewset for handling users endpoint.
    """
    serializer_class = [UsersViewSetSerializer]
