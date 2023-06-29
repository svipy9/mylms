from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} ({self.email})"



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} (f{self.slug})"


class Squad(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    start_date = models.DateField()


class Admission(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, null=True, on_delete=models.SET_NULL)
    squad = models.ForeignKey(to=Squad, null=True, on_delete=models.SET_NULL)

    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} admitted to {self.course.name} on {self.admission_date}"
