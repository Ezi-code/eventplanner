from django.contrib import admin
from main.models import Attendants, NewsLetter

# Register your models here.

admin.site.register([Attendants, NewsLetter])
