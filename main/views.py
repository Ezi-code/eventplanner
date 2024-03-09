from typing import Any
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from main.models import Event, NewsLetter
from services.services import save_new_rsvp, news_letter
from django.core.mail import EmailMessage


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, "main/index.html")


class EventsList(View):
    model = Event

    def get(self, request):
        events = self.model.objects.filter(opened=True)
        closed = self.model.objects.filter(passed=True)
        context = {
            "events": events,
            "closed": closed,
        }
        return render(request, "main/events_list.html", context)


class EventDetails(View):
    def get(self, request, title):
        event = Event.objects.get(title=title)
        return render(request, "main/event_details.html", {"event": event})


class RegisterView(View):
    def get(self, request):
        return HttpResponse("Register View")


class RsvpView(View):
    def get(self, request, title: str):
        if request.user.is_authenticated:
            event = Event.objects.get(title=title)
            return render(request, "main/rsvp.html", {"event": event})
        else:
            return redirect(
                "accounts:login",
            )

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
