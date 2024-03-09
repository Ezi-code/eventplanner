from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create(self, **kwargs: Any) -> Any:
        return super().create(**kwargs)

    def create_superuser(self, **kwargs):
        return self.create(**kwargs)


class User(AbstractBaseUser):

    class Gender(models.TextChoices):
        MALE = ("MALE", "Male")
        FEMALE = ("FEMALE", "Female")
        OTHER = ("OTHER", "Other")

    username = models.CharField(max_length=100, unique=True, blank=False)
    email = models.EmailField()
    password = models.CharField(max_length=100, blank=False, null=False)
    gender = models.CharField(
        max_length=10, choices=Gender.choices, default=Gender.OTHER
    )

    objects = UserManager()
    REQUIRED_FIELDS = ["username", "email", "password"]
