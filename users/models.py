from django.contrib.auth.models import AbstractUser
from django.db import models


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


class User(AbstractUser, TimeStampModel):
    """
        Model to override Django's default User model.
    """
    email_address = models.EmailField()
    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    is_activated = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)