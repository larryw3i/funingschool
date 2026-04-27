from datetime import date

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import CreateView
from fnschool import _, count_chinese_characters

from .fntoken import account_activation_token
from .models import Fnuser


class FnuserLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(request, *args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = Fnuser.objects.get(username=username)
            if user and user.check_password(password):
                if settings.EMAIL_BACKEND:
                    if not user.email_verified:
                        from .views import send_email_verification

                        send_email_verification(self.request, user)

                        self.add_error(
                            "username",
                            _(
                                "Your email has not been verified. We have sent a verification email to your email address. Please check your email and complete the verification process. (If you haven't received the email, please check your spam folder.)"
                            ),
                        )

        self.leaned_data = super().clean()
        return self.cleaned_data


class FnuserSignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        email_field = self.fields.get("email")
        if email_field:
            email_field.label = (
                _("Email Address (Required)")
                if settings.EMAIL_BACKEND
                else _("Email Address (Optional)")
            )
            email_field.help_text = _("Please enter your email address.")

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if settings.EMAIL_BACKEND:
            if not email:
                self.add_error("email", _("Please enter email."))
        else:
            if Fnuser.objects.filter(email=email).exists():
                self.add_error(
                    "email", _("A user with that email already exists.")
                )

        return cleaned_data

    class Meta:
        model = Fnuser
        fields = ("username", "email", "password1", "password2")


class FnuserForm(ModelForm):
    username = forms.CharField(
        max_length=128,
        label=_("User Name"),
        widget=forms.TextInput(attrs={"placeholder": _("User Name")}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={"placeholder": _("Password")}),
    )
    password_confirm = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Confirm Password")}
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].widget.attrs.update(
            {"class": "form-control-file"}
        )

    class Meta:
        current_year = date.today().year
        year_range = list(range(current_year - 100, current_year + 1))
        model = Fnuser
        fields = [
            "username",
            "phone",
            "affiliation",
            "superior_department",
            "date_of_birth",
            "gender",
            "address",
            "avatar",
            "bio",
        ]
        widgets = {
            "date_of_birth": forms.SelectDateWidget(
                years=year_range,
                attrs={"style": "width: 33.33%; display: inline-block;"},
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password") != cleaned_data.get("password_confirm"):
            raise forms.ValidationError("Passwords do not match")


# The end.
