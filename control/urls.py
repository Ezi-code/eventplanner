from django.urls import path
from control.views import (
    EventDetails,
    CreateEvent,
    Budget,
    DashboardView,
    EditEvent,
    DeleteEvent,
)

app_name = "control"

urlpatterns = [
    path("event_details/<str:title>", EventDetails.as_view(), name="event_details"),
    path("create_event", CreateEvent.as_view(), name="create_event"),
    path("edit_event/<str:title>", EditEvent.as_view(), name="edit_event"),
    path("delete_event/<str:title>", DeleteEvent.as_view(), name="delete_event"),
    path("budget", Budget.as_view(), name="budget"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
]