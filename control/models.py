from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from accounts.models import User
from settings import base


class Event(models.Model):
    class EventState(models.TextChoices):
        OPEN = ("OPEN", "Open")
        CLOSED = ("CLOSED", "Closed")

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=150, null=False, default="")
    image = models.ImageField(upload_to="media/events")
    price_tag = models.FloatField(max_length=float("inf"), default=0)
    state = models.CharField(
        max_length=100, choices=EventState.choices, default=EventState.OPEN
    )
    start_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(default=timezone.now)
    duration = models.IntegerField(
        help_text="Number of days event will take place", blank=True, default=1
    )
    end_date = models.DateField(default=timezone.now)
    end_time = models.TimeField(default=timezone.now)
    details = models.TextField(blank=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.title}"


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
def set_balance(sender, instance: EventPlan, *args, **kwargs):
    instance.balance = instance.expected_cost - instance.expenditure


class Budget(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, db_index=True)
    cost_of_venue = models.FloatField(max_length=float("inf"), default=0.0)
    organizational_cost = models.FloatField(max_length=float("inf"), default=0.0)
    expected_guests = models.IntegerField(default=0)
    cost_of_security = models.FloatField(max_length=float("inf"), default=0.0)
    refreshment_cost = models.FloatField(max_length=float("inf"), default=0.0)
    transportation_cost = models.FloatField(max_length=float("inf"), default=0.0)
    misc_cost = models.FloatField(max_length=float("inf"), default=0.0)
    total_cost = models.FloatField(max_length=float("inf"), default=0.0)

    def __str__(self) -> str:
        return f"{self.event} ==> {self.total_cost}"


@receiver(pre_save, sender=Budget)
def set_totla_cost(sender, instance: Budget, *args, **kwargs):
    instance.total_cost = (
        instance.cost_of_venue
        + instance.cost_of_security
        + instance.refreshment_cost
        + instance.transportation_cost
        + instance.misc_cost
        + instance.organizational_cost
    )
