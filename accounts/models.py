from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields: Any):
        if not email:
            raise ValueError("Username field cannot be empty")
        if not password:
            raise ValueError("Password field cannot be empty")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Gender(models.TextChoices):
        MALE = ("MALE", "Male")
        FEMALE = ("FEMALE", "Female")
        OTHER = ("OTHER", "Other")

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=100, unique=False, blank=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.OTHER
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = "email"
    # EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
