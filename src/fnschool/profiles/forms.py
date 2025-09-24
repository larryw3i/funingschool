from fnschool import _
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile


class ProfileLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": _("User Name")})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": _("Password")})
    )


class ProfileForm(ModelForm):
    username = forms.CharField(max_length=128)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = [
            "username",
            "phone",
            "affiliation",
            "superior_department",
            "date_of_birth",
            "address",
            "avatar",
            "bio",
        ]

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match")


# The end.
