from django.contrib import admin

from payment.payment_methods.models import PaymentMethod

admin.site.register(PaymentMethod)
