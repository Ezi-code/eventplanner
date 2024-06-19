from django.contrib import admin
from main.models import Attendee, NewsLetter, Enquiry, Team


# Register your models here.
class AdminAttendees(admin.ModelAdmin):
    list_display = ["name", "event", "tickets"]
    search_fields = ["name", "email", "phone"]


class AdminNewsletter(admin.ModelAdmin):
    list_display = ["email"]
    search_fields = ["email"]


class AdminEnquiry(admin.ModelAdmin):
    list_display = ["name", "message"]
    search_fields = ["name", "email", "created_at"]


class AdminTeam(admin.ModelAdmin):
    list_display = ["name", "position", "address"]
    search_fields = ["name", "address", "position"]


admin.site.register(Attendee, AdminAttendees)
admin.site.register(Enquiry, AdminEnquiry)
admin.site.register(Team, AdminTeam)
admin.site.register(NewsLetter, AdminNewsletter)
