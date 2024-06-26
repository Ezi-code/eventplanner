from django import forms
from control.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        exclude = ["organizer", "state", "created_at", "expiry_date"]

        widgets = {

            "title": forms.TextInput(attrs={"placeholder": "Enter the title of the event"}),

            "description": forms.TextInput(attrs={"placeholder": "Enter the description of the event"}),

            "location": forms.TextInput(attrs={"placeholder": "Enter the location of the event"}),

            "image": forms.FileInput(attrs={"placeholder": "Upload an image for the event"}),

            "price_tag": forms.NumberInput(attrs={"placeholder": "Enter the price of the event"}),

            "date": forms.DateInput(attrs={"type": "date"}),

            "time": forms.TimeInput(attrs={"type": "time"}),

            "details": forms.Textarea(attrs={"rows": 4, "cols": 15}),
        }

        labels = {
            "title": "Event Title",
            "description": "Event Description",
            "location": "Event Location",
            "image": "Event Image",
            "price_tag": "Event Price",
            "date": "Event Date",
            "time": "Event Time",
        }     

