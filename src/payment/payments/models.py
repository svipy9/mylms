from django.db import models, transaction

import learning.interface as learning


class PaymentStatus(models.TextChoices):
    INIT = "init", "Initial"
    SUCCESS = "success", "Successful"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Payment(models.Model):
    admission = models.ForeignKey("admissions.Admission", on_delete=models.CASCADE)
    url = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.INIT,
    )

    def mark_success(self):
        # Rule #3
        self.status = PaymentStatus.SUCCESS
        learning.admission_grant_premium(self.admission_id)

        self.save()

    @transaction.atomic
    def mark_refunded(self):
        refund, _ = Refund.objects.get_or_create(payment=self)
        self.status = PaymentStatus.REFUNDED
        learning.admission_revoke_premium(self.admission)

        self.save()
        return refund


class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Revenue(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
