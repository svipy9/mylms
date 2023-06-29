from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_manager",)}),)


admin.site.register(User, CustomUserAdmin)
