from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

from .models import Profile


def role_required(role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect(reverse("login"))
            try:
                if request.user.profile.role != role:
                    messages.error(request, "You do not have access to that page.")
                    return redirect(reverse("landing"))
            except Profile.DoesNotExist:
                messages.error(request, "Complete your profile first.")
                return redirect(reverse("landing"))
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
