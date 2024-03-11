from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("all_events", EventsList.as_view(), name="all_events"),
    path("event-details/<str:title>", EventDetails.as_view(), name="event-details"),
    path("rsvp/<str:title>", RsvpView.as_view(), name="rsvp"),
    path("send_mail", Sendmail.as_view(), name="send_mail"),
    path("enquiries", Enquiries.as_view(), name="enquiries"),
]
