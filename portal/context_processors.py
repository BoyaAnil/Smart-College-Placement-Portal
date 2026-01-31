from .models import Profile


def user_role(request):
    role = None
    if request.user.is_authenticated:
        try:
            role = request.user.profile.role
        except Profile.DoesNotExist:
            role = None
    return {"user_role": role}
