from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from control.models import Event
from django.db.models.signals import pre_save


class Attendants(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15, unique=True, blank=False, null=False)
    tickets = models.IntegerField(default=0)
    reserved_at = models.DateTimeField(default=timezone.now)
    total_cost = models.FloatField(max_length=float("inf"), default=0)

    def __str__(self) -> str:
        return self.name + " - " + self.event.title + " - " + str(self.tickets)


class NewsLetter(models.Model):
    user = models.CharField(max_length=200, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)

    def __str__(self):
        return self.user + " - " + self.email


class Enquiry(models.Model):
    name = models.CharField(max_length=100, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=15, null=False)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.name}"


@receiver(pre_save, sender=Attendants)
def set_totla_cost(sender, instance: Attendants, *args, **kwargs):
    instance.total_cost = instance.event.price_tag * instance.tickets
