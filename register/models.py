from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username     = None
    phone_number = models.CharField(max_length=11, unique=True)
    first_name   = models.CharField(max_length=255)
    last_name    = models.CharField(max_length=255)
    email        = models.EmailField(unique=True)

    USERNAME_FIELD = "phone_number"

    def __str__(self) -> str:
        return f"{self.first_name} {self.first_name}"
