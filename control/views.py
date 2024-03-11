from django.shortcuts import render, redirect
from django.views.generic import View
from control.models import EventPlan, Event
from control.services import save_new_event, update_event
from main.models import Attendants
from .contenxt_processor import get_notification


# Create your views here.
class EventDetails(View):
    model = Event

    def get(self, request, title):
        event = self.model.objects.get(title=title)
        attendants = Attendants.objects.filter(event=event).count()
        context = {"event": event, "attendants": attendants}
        get_notification(request)
        return render(request, "control/event_details.html", context)


class CreateEvent(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "control/event_form.html")
        else:
            return redirect("accounts:login")

    def post(self, request):
        if request.user.is_authenticated:
            try:
                new_event = save_new_event(request.POST, request.FILES, request.user)
                new_event.full_clean()
                new_event.save()
                return redirect("main:all_events")
            except Exception as e:
                return render(request, "control/event_form.html", {"errors": e})
        else:
            return redirect("accounts:login")


class DeleteEvent(View):
    model = Event

    def get(self, request, title):
        event = self.model.objects.get(title=title)
        event.delete()
        return redirect("control:dashboard")


class EditEvent(View):
    model = Event

    def get(self, request, title):
        event = self.model.objects.get(title=title)
        return render(request, "control/edit_event.html", {"event": event})

    def post(self, request, title):
        event = self.model.objects.get(title=title)
        update_event(event, request)
        event.full_clean()
        event.save()
        return redirect("control:dashboard")


class DashboardView(View):
    def get(self, request):
        events = Event.objects.filter(organizer=request.user).all()
        return render(request, "control/dashboard.html", {"events": events})
