from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.contrib.auth import login, logout, authenticate
from accounts.models import User
from django.contrib import messages


class RegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html")

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        if password != password1:
            messages.error(request, "Passwords do not match")
            return render(request, "accounts/register.html")
        else:
            new_user = User.objects.create_user(
                username=username, email=email, password=password
            )
            new_user.full_clean()
            new_user.save()
            messages.success(request, "Account created successfully")
            return redirect("accounts:login")


class LoginView(View):

    def get(self, request):
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Loged in successful")
            return redirect("main:home")

        else:
            messages.error(request, "Invalid username or password")
            return render(request, "accounts/login.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Logged out successfully")
        return redirect("main:home")
