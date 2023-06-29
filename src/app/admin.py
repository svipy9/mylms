from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.models import Course, Lesson, Payment, PaymentMethod, Squad, User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("is_manager",)}),)


admin.site.register(User, CustomUserAdmin)


class SquadAdmin(admin.ModelAdmin):
    list_display = ("name",)  # fields to display in list view
    search_fields = ("name",)  # fields to search in the admin site


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("admission", "url", "status")
    search_fields = ("admission_id", "status", "url")
    list_filter = ("status",)


admin.site.register(Squad, SquadAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(PaymentMethod)
admin.site.register(Lesson)
admin.site.register(Course)
