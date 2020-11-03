from django.urls import include
from django.urls import path
from rest_framework import routers

from .views import UsersViewSet


router = routers.DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
