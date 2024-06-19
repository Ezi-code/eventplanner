from django.urls import path
from control import views

app_name = "control"

urlpatterns = [
    path(
        "event_details/<str:title>", views.EventDetails.as_view(), name="event_details"
    ),
    path("create_event", views.CreateEvent.as_view(), name="create_event"),
    path("edit_event/<str:title>", views.EditEvent.as_view(), name="edit_event"),
    path("delete_event/<str:title>", views.DeleteEvent.as_view(), name="delete_event"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
    path("notifications", views.Notification.as_view(), name="notifications"),
    path("guest-list/<str:event>", views.GuestList.as_view(), name="guest-list"),
    path(
        "create_budget/<str:event>", views.CreateBudget.as_view(), name="create_budget"
    ),
    path("edit_budget/<int:id>", views.EditBudgetView.as_view(), name="edit_budget"),
]
