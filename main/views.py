from typing import Any
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from main.models import Event, NewsLetter
from main.services import save_new_rsvp, news_letter, get_enquriy


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, "main/index.html")


class EventsList(View):
    model = Event

    def get(self, request):
        events = self.model.objects.filter(state="OPEN")
        closed = self.model.objects.filter(state="CLOSED")
        context = {
            "events": events,
            "closed": closed,
        }
        return render(request, "main/events_list.html", context)


class EventDetails(View):
    def get(self, request, title):
        event = Event.objects.get(title=title)
        return render(request, "main/event_details.html", {"event": event})


class RsvpView(View):
    def get(self, request, title: str):
        event = Event.objects.get(title=title)
        return render(request, "main/rsvp.html", {"event": event})

    def post(self, request, title: str):
        event = Event.objects.get(title=title)
        new_rsvp = save_new_rsvp(request.POST, event)
        if new_rsvp:
            return redirect("main:home")
        else:
            return render(request, "main/rsvp.html", {"event": event})


class Sendmail(View):
    def post(self, request):
        email = request.POST.get("email")
        news_letter(email)
        print(email)
        new_sub = NewsLetter(email=email, user=request.user)
        new_sub.full_clean()
        new_sub.save()
        return redirect("main:home")


class Enquiries(View):
    def get(self, request):
        return render(request, "main/enquiries.html")

    def post(self, request):
        new_enquiry = get_enquriy(request)
        new_enquiry.full_clean()
        new_enquiry.save()
        return redirect("main:home")
