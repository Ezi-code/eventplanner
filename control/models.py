from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from settings import base

# Create your models here.


class Event(models.Model):
    # from main.models import RSVP

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    details = models.TextField(blank=False)
    location = models.CharField(max_length=150, null=False, default="")
    image = models.ImageField(upload_to=base.MEDIA_ROOT)
    price_tag = models.FloatField(max_length=float("inf"), default=0)
    opened = models.BooleanField(default=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    passed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title}"


class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_completed=False)


class Task(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    desccription = models.TextField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    objects = TaskManager()


class EventPlan(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    expected_cost = models.FloatField(max_length=float("inf"))
    expenditure = models.FloatField(max_length=float("inf"))
    exp_items = models.TextField()
    venue = models.CharField(max_length=200, blank=False, default=None)
    balance = models.FloatField()

    def default_balance(self):
        self.balance = self.expected_cost - self.expenditure
        return self.balance


@receiver(pre_save, sender=EventPlan)
def set_balance(sender: EventPlan, instance: EventPlan, *args, **kwargs):
    instance.balance = instance.expected_cost - instance.expenditure


class Enquiry(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15, unique=True, blank=False, null=False)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name
