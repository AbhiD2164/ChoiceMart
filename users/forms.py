from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "email", "contact_no", "password1", "password2"]

        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "off"}),
            "email": forms.EmailInput(attrs={"autocomplete": "off"}),
            "contact_no": forms.TextInput(attrs={"autocomplete": "off"}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"})
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "on"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "off"})
    )