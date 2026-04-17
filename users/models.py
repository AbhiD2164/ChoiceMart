from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import random


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, name, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    contact_no = models.CharField(max_length=15)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    def __str__(self):
        return self.email


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=random.randint(50000, 150000))
    upi_id = models.CharField(max_length=100, blank=True, null=True)