from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils import timezone


# created a user manager for creating users without problem of custom username fields
class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        # if phone number field not provided 
        if not phone_number:
            raise ValueError('The Phone Number is required')

        # an instance of user model
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, password=None, **extra_fields):
        # making some admin fields to be their default values
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    username     = None
    phone_number = models.CharField(max_length=11, unique=True)
    first_name   = models.CharField(max_length=255, blank=True, null=True)
    last_name    = models.CharField(max_length=255, blank=True, null=True)
    email        = models.EmailField(unique=True, blank=True, null=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = UserManager()


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

    # lockout the account
    def lockOut(self):
        self.lockout_until = timezone.now()+timedelta(hours=1)
        self.save()


    # returns a bool whethere user is blocked or not
    def isLockedOut(self):
        if self.lockout_until and self.lockout_until > timezone.now():
            return True
        
        return False
    
    # increases the attempts field by one
    def increaseAttempts(self):
        self.failed_attempts += 1
        self.save()

    # reset the lockout basically sets everythin to default
    def resetLockOut(self):
        self.lockout_until = None
        self.failed_attempts = 0
        self.save()

