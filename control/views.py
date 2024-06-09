from django.shortcuts import render, redirect
from django.views.generic import View
from control.models import Event, Budget
from control import services as srv
from main.models import Attendants, Enquiry
from .contenxt_processor import get_notification
from django.contrib import messages
from control.services import LoginMixin
from control.forms import EventForm


# Create your views here.
class EventDetails(View):
    model = Event

    def get(self, request, title):
        event = self.model.objects.get(title=title)
        attendants = Attendants.objects.filter(event=event).count()
        total = srv.get_total_cost(event)
        budget = Budget.objects.get(event=event)

        context = {
            "event": event,
            "attendants": attendants,
            "budget": budget,
            "total": total,
        }
        
        get_notification(request)
        return render(request, "control/event_details.html", context)


class CreateEvent(LoginMixin, View):
    def get(self, request):
        form = EventForm()
        ctx = {"form": form}
        return render(request, "control/event_form.html", ctx)


    def post(self, request):       
        form = EventForm(request.POST, request.FILES)
        # new_event = form.save(commit=False)
        if form.is_valid():
            new_event = form.save(commit=False)

            if Event.objects.filter(title=new_event.title).exists():
                messages.error(request, "Event with this title already exists")
                return render(request, "control/event_form.html", {"form": form})
            
            new_event.organizer = request.user
            new_event.save()
            messages.success(request, "Event Created Successfully")
            return redirect("control:create_budget", new_event)
       
        # messages.error(request, "An error occured")
        return render(request, "control/event_form.html", {"form": form})


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
        srv.update_event(event, request)
        event.full_clean()
        event.save()
        messages.success(request, "Event Updated Successfully")
        return redirect("control:dashboard")


class DashboardView(LoginMixin, View):
    def get(self, request):
        events = Event.objects.filter(organizer=request.user).all()
        return render(request, "control/dashboard.html", {"events": events})


class Notification(LoginMixin, View):
    def get(self, request):
        count = Enquiry.objects.filter(read=False).count()
        messages = Enquiry.objects.filter(read=False).all()[::-1]
        cntx = {"count": count, "messages": messages}
        return render(request, "control/notifications.html", cntx)


class GuestList(LoginMixin, View):
    def get(self, request, event):
        guests = Attendants.objects.filter(event=event).all()
        event = Event.objects.get(id=event)
        ticket_amoaunt = []
        print(ticket_amoaunt)
        ctx = {"event": event, "guests": guests}

        return render(request, "control/guest_list.html", ctx)


class CreateBudget(LoginMixin, View):
    def get(self, request, event):
        event = Event.objects.get(title=event)
        return render(request, "control/create_budget.html", {"event": event})

    def post(self, request, event):
        event = Event.objects.get(title=event)
        try:
            new_budget = srv.create_budget(request, event)
            new_budget.full_clean()
            new_budget.save()
            messages.success(request, "Budget Created Successfully")
            return redirect("main:all_events")
        except Exception as e:
            messages.error(request, 'Invalid field(s) entry')
            return render(request, "control/create_budget.html", {"event": event})
            


class EditBudgetView(LoginMixin, View):
    model = Budget

    def get(self, req, id):
        budget = self.model.objects.get(id=id)
        print(budget)
        ctx = {"budget": budget}
        return render(req, "control/edit_budget.html", ctx)

    def post(self, req, id):
        budget = Budget.objects.get(id=id)
        event = budget.event
        srv.update_budget(req, budget)
        budget.clean_fields()
        budget.save()
        messages.success(req, "Budget Updated Successfully")
        return redirect("control:event_details", event)
