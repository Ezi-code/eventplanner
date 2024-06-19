from django.contrib import admin
from control.models import EventPlan, Event, Budget


# Register your models here.
class AdminEventPlan(admin.ModelAdmin):
    list_display = ["event", "expenditure", "venue", "balance"]
    search_fields = ["event", "expenditure", "venue", "balance"]


class AdminEvent(admin.ModelAdmin):
    list_display = ["organizer", "title", "description", "location"]
    search_fields = ["organizer", "title", "description", "location"]


class AdminBudget(admin.ModelAdmin):
    list_display = ["event", "total_cost"]
    search_fields = ["event", "total_cost"]


admin.site.register(Event, AdminEvent)
admin.site.register(Budget, AdminBudget)
admin.site.register(EventPlan, AdminEventPlan)
