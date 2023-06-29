from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} ({self.email})"


class Course(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.name} ({self.slug})"


class Lesson(models.Model):
    course_id = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    is_free = models.BooleanField(default=False)


class Squad(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_date = models.DateField()


class Admission(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "course"], name="unique_admission")
        ]  # Rule #1

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, null=True, on_delete=models.SET_NULL)
    squad = models.ForeignKey(to=Squad, null=True, on_delete=models.SET_NULL)

    is_premium = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} admitted to {self.course.name}"


class PaymentStatus(models.TextChoices):
    INIT = "init", "Initial"
    SUCCESS = "success", "Successful"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class Payment(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
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
            self.admission.is_premium = True  # Rule #3
            self.admission.paid_at = timezone.now()
            nearest_squad = Squad.objects.filter(
                course=self.admission.course,
                start_date__gt=timezone.now(),
            ).first()
            self.admission.squad = nearest_squad
            self.admission.save()


class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Revenue(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
