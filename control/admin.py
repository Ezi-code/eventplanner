from django.contrib import admin
from control.models import EventPlan, Event, Budget

# Register your models here.
admin.site.register([EventPlan, Event, Budget])
