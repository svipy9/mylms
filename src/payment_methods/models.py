from django.db import models


class PaymentMethod(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    external_id = models.CharField(max_length=200)
