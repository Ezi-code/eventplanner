import datetime
from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.utils import timezone


def main(request, event, email):

    start_datetime = datetime.datetime.combine(event.start_date, event.start_time)
    end_datetime = datetime.datetime.combine(event.end_date, event.end_time)

    if "credentials" not in request.session:
        redirect("main:initiate_auth")


    credentials = Credentials(**request.session["credentials"])

    try:
        service = build("calendar", "v3", credentials=credentials)
        event = {
            "summary": event.title,
            "location": event.location,
            "description": event.description,
            "colorId": 6,
            "start": {
                "dateTime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": str(timezone.get_current_timezone()),
            },
            "end": {
                "dateTime": end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": str(timezone.get_current_timezone()),
            },
            "recurrence": [f"RRULE:FREQ=DAILY;COUNT={event.duration}"],
            "attendees": [{"email": email}],
        }
        print(event.items(), sep="\n")
        event = service.events().insert(calendarId="primary", body=event).execute()
        
        print(f"event created on google calendar {event.get('htmlLink')}")
        return event.get("htmlLink")
    except HttpError as error:
        print(f"An error occurred: {error}")
