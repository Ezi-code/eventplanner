from django.urls import path
from control.views import (
    EventDetails,
    CreateEvent,
    DashboardView,
    EditEvent,
    DeleteEvent,
    Notification,
    GuestList,
    CreateBudget,
)

app_name = "control"

urlpatterns = [
    path("event_details/<str:title>", EventDetails.as_view(), name="event_details"),
    path("create_event", CreateEvent.as_view(), name="create_event"),
    path("edit_event/<str:title>", EditEvent.as_view(), name="edit_event"),
    path("delete_event/<str:title>", DeleteEvent.as_view(), name="delete_event"),
    path("dashboard", DashboardView.as_view(), name="dashboard"),
    path("notifications", Notification.as_view(), name="notifications"),
    path("guest-list/<str:event>", GuestList.as_view(), name="guest-list"),
    path("create_budget<str:event>", CreateBudget.as_view(), name="create_budget"),
]
