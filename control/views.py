from django.shortcuts import render, redirect
from django.views.generic import View
from control.models import Event, Budget
from control.services import get_total_cost, save_new_event, update_event, create_budget
from main.models import Attendants, Enquiry
from .contenxt_processor import get_notification


# Create your views here.
class EventDetails(View):
    model = Event

    def get(self, request, title):
        event = self.model.objects.get(title=title)
        attendants = Attendants.objects.filter(event=event).count()
        total = get_total_cost(event)
        budget = Budget.objects.get(event=event).total_cost

        context = {
            "event": event,
            "attendants": attendants,
            "budget": budget,
            "total": total,
        }
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
                return redirect("control:create_budget", new_event)
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


class Notification(View):
    def get(self, request):
        count = Enquiry.objects.filter(read=False).count()
        messages = Enquiry.objects.filter(read=False).all()[::-1]
        cntx = {"count": count, "messages": messages}
        return render(request, "control/notifications.html", cntx)


class GuestList(View):
    def get(self, request, event):
        guests = Attendants.objects.filter(event=event).all()
        event = Event.objects.get(id=event)
        ticket_amoaunt = []
        print(ticket_amoaunt)
        ctx = {"event": event, "guests": guests}

        return render(request, "control/guest_list.html", ctx)


class CreateBudget(View):
    def get(self, request, event):
        event = Event.objects.get(title=event)
        return render(request, "control/create_budget.html", {"event": event})

    def post(self, request, event):
        event = Event.objects.get(title=event)
        new_budget = create_budget(request, event)
        new_budget.full_clean()
        new_budget.save()
        return redirect("main:all_events")
