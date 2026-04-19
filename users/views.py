import random

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .forms import RegisterForm, LoginForm
from .models import Wallet


# REGISTER
def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        Wallet.objects.create(
            user=user,
            balance=random.uniform(50000,2500000),
            upi_id=form.cleaned_data.get("upi_id")
        )

        return redirect("login")

    return render(request, "users/register.html", {"form": form})


# LOGIN
def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            user.last_login = timezone.now()
            user.save()

            return redirect("product_list")
        else:
            return render(request, "users/login.html", {
                "form": form,
                "error": "Invalid email or password"
            })

    return render(request, "users/login.html", {"form": form})


# LOGOUT
def logout_view(request):
    logout(request)
    return redirect("")