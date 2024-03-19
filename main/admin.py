from django.contrib import admin
from main.models import Attendants, NewsLetter, Enquiry

# Register your models here.

admin.site.register([Attendants, NewsLetter, Enquiry])
