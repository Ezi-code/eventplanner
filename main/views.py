import os
from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.base import View
from main.models import Event, NewsLetter
from main.services import save_new_rsvp, news_letter, get_enquriy
from django.contrib import messages
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def credentials_to_dict(credentials):
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        "C:\\Users\\Ezi\\Documents\\code\\eventplanner\\main\\credentials.json",
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="https://localhost:8000/oauth2callback/",
    )

    # flow.fetch_token(authorization_response=request.build_absolute_uri())

    # f = open("C:\\Users\\Ezi\\Documents\\code\\eventplanner\\main\\token.json", "rwb")
    # f.write(flow.credentials)
    # f.close()
    # credentials = flow.credentials

    # request.session["credentials"] = credentials_to_dict(credentials)

    return redirect("main:home")


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
        new_rsvp = save_new_rsvp(request, event)
        if new_rsvp:
            messages.success(request, "RSVP Successful")
            return redirect("main:home")
        else:
            messages.error(request, "An error occured! ")
            return render(request, "main/rsvp.html", {"event": event})


class Sendmail(View):
    def post(self, request):
        email = request.POST.get("email")
        if NewsLetter.objects.filter(email=email).exists():
            messages.error(request, "Email already exist")
            return redirect("main:home")
        try:
            new_sub = NewsLetter(email=email)
            new_sub.full_clean()
            new_sub.save()
            news_letter(email)
            messages.success(request, "You've subscribed to our news letter")
        except Exception as e:
            messages.error(request, "An error occured while subscribing ")

        return redirect("main:home")


class Enquiries(View):
    def get(self, request):
        return render(request, "main/enquiries.html")

    def post(self, request):
        new_enquiry = get_enquriy(request)
        new_enquiry.full_clean()
        new_enquiry.save()
        messages.success(request, "Enquiry Sent")
        return redirect("main:home")


def create_event(request):
    creds = None

    if "credentials" not in request.session:
        return redirect("main:oauth2callback")

    credentials = Credentials(**request.session["credentials"])

    event = {
        "summary": "Sample Event",
        "location": "800 Howard St., San Francisco, CA 94103",
        "description": "A chance to hear more about Google's developer products.",
        "start": {
            "dateTime": "2024-06-18T09:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": "2024-06-18T17:00:00-07:00",
            "timeZone": "America/Los_Angeles",
        },
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
        "attendees": [
            {"email": "lpage@example.com"},
            {"email": "sbrin@example.com"},
        ],
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }
    return redirect("main:event_list")


def initiate_oauth(request):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Development only
    flow = Flow.from_client_secrets_file(
        "C:\\Users\\Ezi\\Documents\\code\\eventplanner\\main\\creds.json",
        scopes=["https://www.googleapis.com/auth/calendar.events"],
        redirect_uri="http://localhost:8000/oauth2callback/",
    )

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )

    request.session["state"] = state
    return redirect(authorization_url)


def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        "C:\\Users\\Ezi\\Documents\\code\\eventplanner\\main\\creds.json",
        scopes=["https://www.googleapis.com/auth/calendar.events"],
        redirect_uri="http://localhost:8000/oauth2callback/",
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials
    # Save the credentials in session or database
    request.session["credentials"] = credentials_to_dict(credentials)

    return redirect("main:home")


class AboutView(View):
    def get(self, request):
        members = [1, 2, 3, 4, 5]
        return render(request, "main/about.html", {"members": members})
