from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from .managers import UserManager


class TimeStampModel(models.Model):
    """
    Base model for setting time stamps. Inherit this class when time
    tracking is desired.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    """Model to override Django's User model."""
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    is_active = models.BooleanField(default=True)
    is_activated = models.BooleanField(
        default=False,
        help_text='Set to True for users that activated resources via the API.')
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def update_password(self, password):
        """Method to ensure password hashing on update."""
        self.set_password(password)
        self.save()
