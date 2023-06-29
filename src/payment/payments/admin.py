from django.contrib import admin

from payment.payments.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("admission", "url", "status")
    search_fields = ("admission_id", "status", "url")
    list_filter = ("status",)


admin.site.register(Payment, PaymentAdmin)
