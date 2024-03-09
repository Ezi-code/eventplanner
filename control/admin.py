from django.contrib import admin
from control.models import EventPlan, Event, Enquiry

# Register your models here.
admin.site.register([EventPlan, Event, Enquiry])
