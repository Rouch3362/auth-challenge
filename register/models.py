from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime
from django.utils import timezone

class User(AbstractUser):
    username     = None
    phone_number = models.CharField(max_length=11, unique=True)
    first_name   = models.CharField(max_length=255, blank=True, null=True)
    last_name    = models.CharField(max_length=255, blank=True, null=True)
    email        = models.EmailField(unique=True, blank=True, null=True)

    USERNAME_FIELD = "phone_number"


    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"



class OTP(models.Model):
    phone_number = models.CharField(max_length=11)
    code         = models.CharField(max_length=6)
    created_at   = models.DateTimeField(auto_now_add=True)
    valid_until  = models.DateTimeField(default=timezone.now()+timedelta(hours=1))


    def __str__(self) -> str:
        return f'{self.phone_number} {self.code}'
    


class UserLockout(models.Model):
    phone_number    = models.CharField(max_length=11 , blank=True , null=True)
    ip_address      = models.GenericIPAddressField()
    failed_attempts = models.IntegerField(default=0)
    lockout_until   = models.DateTimeField(blank=True, null=True)


    def lockOut(self):
        self.lockout_until = timezone.now()+timedelta(hours=1)
        self.save()

    def isLockedOut(self):
        if self.lockout_until and self.lockout_until > timezone.now():
            return True
        
        return False
    

    def increaseAttempts(self):
        self.failed_attempts += 1
        self.save()

    def resetLockOut(self):
        self.lockout_until = None
        self.failed_attempts = 0
        self.save()

