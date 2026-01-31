from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm
from portal.models import Profile


def register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect(_post_login_redirect(user))
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back!")
            next_url = request.GET.get("next")
            return redirect(next_url or _post_login_redirect(user))
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    for field in form.fields.values():
        field.widget.attrs.update(
            {"class": "w-full border border-slate-200 rounded-md px-3 py-2"}
        )
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(reverse("landing"))


def _post_login_redirect(user) -> str:
    try:
        if user.profile.role == Profile.ROLE_RECRUITER:
            return reverse("recruiter_dashboard")
        return reverse("student_dashboard")
    except Profile.DoesNotExist:
        return reverse("landing")
