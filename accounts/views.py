from django.shortcuts import render, HttpResponse, redirect
from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        print(username, email, password, password1)
        if password != password1:
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match"},
            )
        else:
            new_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            new_user.full_clean()
            new_user.save()
            return redirect("main:home")


class LoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("main:home")

        else:
            print("Invalid username or password")
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid username or password"},
            )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("main:home")
