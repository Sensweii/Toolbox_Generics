from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .authentications import UserAuthentication
from .serializers import LoginViewSerializer


class LoginView(GenericAPIView):
    """
        Class for handling login requests.
    """
    serializer_class = LoginViewSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = UserAuthentication().authenticate(**serializer.data)
            return Response(token)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
