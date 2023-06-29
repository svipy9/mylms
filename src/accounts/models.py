from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} ({self.email})"
