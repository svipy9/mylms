from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


class UserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_manager",)}),)


admin.site.register(User, UserAdmin)
