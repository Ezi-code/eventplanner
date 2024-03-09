from django.shortcuts import render, redirect
from django.views.generic import View
from control.models import EventPlan, Event
from services.services import save_new_event
from main.models import Attendants


# Create your views here.
class EventDetails(View):
    model = Event

    def get(self, request, title):
        event = self.model.objects.get(title=title)
        print(event.location)
        attendants = Attendants.objects.filter(event=event).count()
        print(attendants)
        context = {"event": event, "attendants": attendants}
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
                print("error: ", e)
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
        event.title = request.POST.get("title")
        event.description = request.POST.get("description")
        event.location = request.POST.get("location")
        event.date = request.POST.get("date")
        event.time = request.POST.get("time")
        event.details = request.POST.get("details")
        event.price_tag = request.POST.get("price")
        event.image = request.FILES.get("image")
        event.full_clean()
        event.save()
        return redirect("control:dashboard")


class Budget(View):
    model = EventPlan

    def get(self, request):
        return render(request, "")


class DashboardView(View):
    def get(self, request):
        print(request.user)
        events = Event.objects.filter(organizer=request.user)
        return render(request, "control/dashboard.html", {"events": events})
