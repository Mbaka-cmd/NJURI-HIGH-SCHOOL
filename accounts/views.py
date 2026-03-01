from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect(request.user.get_dashboard_url())
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect(user.get_dashboard_url())
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("/accounts/login/")


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")
    return redirect(request.user.get_dashboard_url())