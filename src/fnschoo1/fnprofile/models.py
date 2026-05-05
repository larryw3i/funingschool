import os
import sys
import uuid
from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic import CreateView
from fnschool import *
from fnschool import _, count_chinese_characters
from fnschool.fncookie import get_object_orders_from_cookie

resend_verification_email_time_interval = 5 * 60
max_email_count = 8
max_username_length = 256
max_email_length = max_username_length


class Gender(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    UNKNOWN = "U", "--"


class Fnuser(AbstractUser, PermissionsMixin):
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text=_("The groups this user belongs to."),
        related_name="fn_user_groups",
        related_query_name="fn_user",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="fn_user_permissions",
        related_query_name="fn_user",
    )

    email = models.EmailField(
        _("email address"),
        blank=True,
        null=True,
        unique=True,
        max_length=256,
        help_text=_("Primary email address."),
        error_messages={
            "unique": _("This email is already registered."),
        },
    )

    phone = models.CharField(
        max_length=16,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Phone Number"),
    )
    affiliation = models.CharField(
        max_length=256, blank=True, null=True, verbose_name=_("Affiliation")
    )

    superior_department = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name=_("Superior department"),
    )

    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name=_("Date of Birth")
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.UNKNOWN,
        verbose_name=_("Gender"),
    )

    address = models.CharField(
        max_length=256, blank=True, null=True, verbose_name=_("Address")
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name=_("Avatar")
    )
    bio = models.TextField(
        max_length=512, blank=True, verbose_name=_("Biography")
    )

    created_at = models.DateTimeField(
        null=True, auto_now_add=True, verbose_name=_("Time of creating")
    )

    updated_at = models.DateTimeField(
        null=True, auto_now=True, verbose_name=_("Time of updating")
    )

    class Meta:
        verbose_name = _("User Information")
        verbose_name_plural = _("User Information")

    def __str__(self):
        return _("{0}'s Information").format(self.username)

    def get_primary_email(self):
        primary_email = self.emails.get(is_primary=True, is_active=True)
        return primary_email.email

    def has_verified_email(self):
        if not self.emails.exists():
            return False
        return self.emails.filter(is_verified=True, is_active=True).exists()

    def get_first_email(self):
        return self.emails.first()


class Fnemail(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
    )
    user = models.ForeignKey(
        Fnuser,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name=_("User"),
        db_index=True,
    )

    email = models.EmailField(
        _("Email address"),
        max_length=max_email_length,
        db_index=True,
        help_text=_("Please enter a valid email address"),
    )

    is_verified = models.BooleanField(
        _("Is verified"),
        default=False,
        help_text=_("Whether the email has been verified"),
    )

    verification_token = models.CharField(
        _("Verification token"),
        max_length=256,
        blank=True,
        null=True,
        help_text=_("Token for email verification"),
    )

    verification_sent_at = models.DateTimeField(
        _("Verification email sent at"),
        blank=True,
        null=True,
        help_text=_("When the verification email was last sent"),
    )

    verified_at = models.DateTimeField(
        _("Verified at"),
        blank=True,
        null=True,
        help_text=_("When the email was verified"),
    )

    is_active = models.BooleanField(
        _("Is active"),
        default=True,
        help_text=_("Whether this email address is active"),
    )

    is_primary = models.BooleanField(
        _("Is primary"),
        default=False,
        help_text=_("Whether this is the primary email address"),
    )

    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    @property
    def pk(self):
        return self.id

    @pk.setter
    def pk(self, value):
        self.id = value

    class Meta:
        verbose_name = _("User Email")
        verbose_name_plural = _("User Emails")
        ordering = ["-is_primary", "-is_verified", "-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "email"],
                name="unique_user_email",
                violation_error_message=_("You have already added this email."),
            ),
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(is_primary=True, is_active=True),
                name="unique_user_primary_email",
                violation_error_message=_(
                    "You can only have one primary email."
                ),
            ),
        ]

        indexes = [
            models.Index(fields=["user", "is_primary", "is_active"]),
            models.Index(fields=["email", "is_verified"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.user.username}: {self.email}"

    def can_resend_verification_email(self):
        if not self.verification_sent_at:
            return True

        time_since_last = (
            timezone.now() - self.verification_sent_at
        ).total_seconds()
        return time_since_last >= resend_verification_email_time_interval

    def send_verification_email(self, request):
        if not self.can_resend_verification_email():
            return False
        token = self.generate_verification_token()
        current_site = get_current_site(request)
        mail_subject = _("Activate your account.")
        message = render_to_string(
            "fnprofile/fnemail/active.html",
            {
                "user": self.user,
                "http": "https" if request.is_secure() else "http",
                "domain": current_site.domain,
                "email_id": self.pk,
                "token": token,
            },
        ).strip()
        to_email = self.email
        email = EmailMessage(
            mail_subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )
        email.send()
        return True

    def clean(self):
        super().clean()
        self.email = self.email.lower().strip()
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email
        ):
            raise ValidationError({"email": _("Invalid email format.")})

    def generate_verification_token(self):
        self.verification_token = (
            uuid.uuid4().hex
            + uuid.uuid4().hex
            + uuid.uuid4().hex
            + uuid.uuid4().hex
        )
        self.verification_sent_at = timezone.now()
        self.save(update_fields=["verification_token", "verification_sent_at"])

        return self.verification_token

    def sync_to_user_email(self):
        if self.is_primary and self.is_verified and self.is_active:
            if self.user.email != self.email:
                self.user.email = self.email
                self.user.save(update_fields=["email"])
                return True
        return False

    def verify(self, token):
        if not self.verification_token or self.verification_token != token:
            return False

        if self.verification_sent_at:
            expiry_time = self.verification_sent_at + timezone.timedelta(
                seconds=resend_verification_email_time_interval
            )
            if timezone.now() > expiry_time:
                return False

        self.is_verified = True
        self.verified_at = timezone.now()
        self.verification_token = None
        self.save(
            update_fields=["is_verified", "verified_at", "verification_token"]
        )

        if not Fnemail.objects.filter(
            user=self.user, is_primary=True, is_verified=True
        ).exists():
            self.is_primary = True
            self.save(update_fields=["is_primary"])

        self.sync_to_user_email()

        return True

    def set_as_primary(self):
        if not self.is_verified:
            raise ValidationError(
                {
                    "email": _(
                        "Email must be verified before setting as primary."
                    )
                }
            )

        if not self.is_active:
            raise ValidationError(
                {"email": _("Email must be active to set as primary.")}
            )

        Fnemail.objects.filter(user=self.user, is_primary=True).update(
            is_primary=False
        )
        self.is_primary = True
        self.save(update_fields=["is_primary"])
        self.sync_to_user_email()
        return True

    @property
    def status_display(self):
        if not self.is_active:
            return _("Disabled")
        elif not self.is_verified:
            return _("Unverified")
        elif self.is_primary:
            return _("Primary")
        else:
            return _("Verified")

    @property
    def status_color(self):
        if not self.is_active:
            return "secondary"
        elif not self.is_verified:
            return "warning"
        elif self.is_primary:
            return "success"
        else:
            return "info"


# The end.
