from django.contrib import admin
from accounts.models import User


# Register your models here.
class AdminUser(admin.ModelAdmin):
    list_display = ["username", "email", "is_active", "is_superuser"]
    search_fields = ["username", "email"]


admin.site.register(User, AdminUser)
