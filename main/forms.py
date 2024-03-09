from django import forms
from main.models import RSVP

class Rsvp(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = "__all__"
        