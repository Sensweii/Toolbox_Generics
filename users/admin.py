from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    """
        Admin class for User model.
    """
    list_display = ('email_address', 'is_activated')


admin.site.register(User, UserAdmin)
