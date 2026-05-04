import re
from datetime import date

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from fnschool import _, count_chinese_characters

from .fntoken import account_activation_token
from .models import Fnemail, Fnuser, max_email_count


class FnuserLoginForm(AuthenticationForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(request, *args, **kwargs)

    def clean(self):

        self.leaned_data = super().clean()
        return self.cleaned_data


class FnuserSignUpForm(UserCreationForm):

    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@domain.com",
                "autocomplete": "email",
            }
        ),
        max_length=255,
        help_text=_("We'll send a verification email to this address."),
    )

    # Terms agreement
    agree_terms = forms.BooleanField(
        label=_("I agree to the Terms of Service"),
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        ),
        required=True,
        error_messages={
            "required": _("You must agree to the Terms of Service.")
        },
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        email_field = self.fields.get("email")
        if email_field:
            email_field.label = (
                _("Email Address (Required)")
                if settings.EMAIL_BACKEND
                else _("Email Address (Optional)")
            )
            email_field.help_text = _("Please enter your email address.")

        self.fields["username"].help_text = _(
            "Required. 256 characters or fewer. Letters, digits and @/./+/-/_ only."
        )

        self.field_order = [
            "username",
            "email",
            "password1",
            "password2",
            "agree_terms",
        ]

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

    def clean_username(self):
        from .model import max_email_length, max_username_length

        username = self.cleaned_data.get("username")
        if not username:
            raise ValidationError(_("Please enter a username."))
        username_regex = r"^[\w.@+-]+\Z"
        if not re.match(username_regex, username):
            raise ValidationError(
                _(
                    "Username can only contain letters, digits and @/./+/-/_ characters."
                )
            )

        if len(username) < 3:
            raise ValidationError(_("Username must be at least 3 characters."))

        if len(username) > max_username_length:
            raise ValidationError(_("Username cannot exceed 256 characters."))

        if Fnuser.objects.filter(username=username).exists():
            raise ValidationError(_("This username is already taken."))
        return username.strip()

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise ValidationError(_("Please enter an email address."))

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Please enter a valid email address."))

        email = email.lower().strip()
        if Fnemail.objects.filter(email=email, is_active=True).exists():
            raise ValidationError(_("This email is already registered."))

        return email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        if username and email and username.lower() in email.lower():
            self.add_error(
                "username",
                _("Username should not be part of your email address."),
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            fn_email = Fnemail.objects.create(
                user=user,
                email=user.email,
            )

        return user


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


class FnemailAddForm(forms.ModelForm):
    class Meta:
        model = Fnemail
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "new.email@example.com",
                    "autocomplete": "email",
                }
            ),
        }
        labels = {
            "email": _("Email Address"),
        }
        help_texts = {
            "email": _("Add a new email address to your account"),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise ValidationError(_("Please enter an email address."))

        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_("Please enter a valid email address."))

        email = email.lower().strip()
        if (
            self.user
            and Fnemail.objects.filter(user=self.user, email=email).exists()
        ):
            raise ValidationError(_("You have already added this email."))

        # Check if email is used by other users
        if Fnemail.objects.filter(email=email, is_active=True).exists():
            other_user = (
                Fnemail.objects.filter(email=email, is_active=True).first().user
            )
            if other_user != self.user:
                raise ValidationError(
                    _("This email is already used by another user.")
                )

        return email


class FnemailEditForm(forms.ModelForm):

    class Meta:
        model = Fnemail
        fields = ["email", "is_verified", "is_active", "is_primary"]
        widgets = {
            "is_primary": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }
        labels = {
            "is_primary": _("Set as primary email"),
        }
        help_texts = {
            "is_primary": _("Primary email will be used for notifications."),
        }


# The end.
