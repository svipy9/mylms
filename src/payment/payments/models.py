from django.db import models
import learning


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

    def save(self, *args, **kwargs):
        # If this instance is already in the database, get its current state.
        if self.pk is not None:
            original = Payment.objects.get(pk=self.pk)
        else:
            original = None

        # Call the "real" save() method to save the new state.
        super().save(*args, **kwargs)

        # If the status changed from INIT to SUCCESS, call .
        if (
            original is not None
            and original.status == PaymentStatus.INIT
            and self.status == PaymentStatus.SUCCESS
        ):
            learning.admission_grant_premium(self.admission_id)  # Rule #3


class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Revenue(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
