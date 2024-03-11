from main.models import Attendants
from control.models import Event
from django.http import request


def get_notification(request):
    return print(request.user)
