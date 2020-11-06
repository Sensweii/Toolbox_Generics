from django.urls import include
from django.urls import path

from rest_framework import routers

from .views import LoginView


router = routers.DefaultRouter()

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('', include('users.api.v1.urls')),
    path('', include(router.urls)),
]
