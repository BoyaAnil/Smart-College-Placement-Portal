from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from portal.models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update(
                {"class": "w-full border border-slate-200 rounded-md px-3 py-2"}
            )

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user, defaults={"role": self.cleaned_data["role"]}
            )
        return user
