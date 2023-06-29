from django.contrib.auth.models import AbstractUser
from django.db import models


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
        ]

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


class Refund(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Revenue(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
