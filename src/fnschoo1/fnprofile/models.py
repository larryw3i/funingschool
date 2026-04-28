import os
import sys
import uuid
from pathlib import Path

from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
    User,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _
from fnschool import *

# Create your models here.
resend_verification_email_time_interval = 5 * 60
max_email_count = 8


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

    def get_primary_email(self):
        primary_email = self.emails.get(is_primary=True, is_active=True)
        return primary_email.email

    def has_verified_email(self):
        return self.emails.filter(is_verified=True, is_active=True).exists()

    class Meta:
        verbose_name = _("User Information")
        verbose_name_plural = _("User Information")

    def __str__(self):
        return _("{0}'s Information").format(self.username)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_primary_email_instance(self):
        try:
            return self.emails.get(is_primary=True, is_active=True)
        except Fnemail.DoesNotExist:
            return None

    def get_primary_email(self):
        primary_email = self.get_primary_email_instance()
        if primary_email:
            return primary_email.email
        return self.email

    def has_verified_email(self):
        return self.emails.filter(is_verified=True, is_active=True).exists()

    def update_email_from_primary(self):
        primary_email = self.get_primary_email_instance()
        if primary_email and primary_email.is_verified:
            if self.email != primary_email.email:
                self.email = primary_email.email
                self.save(update_fields=["email"])
                return True
        return False


class Fnemail(models.Model):
    user = models.ForeignKey(
        Fnuser,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name=_("User"),
        db_index=True,
    )

    # Email address
    email = models.EmailField(
        _("Email address"),
        max_length=255,
        db_index=True,
        help_text=_("Please enter a valid email address"),
    )

    # Verification related
    is_verified = models.BooleanField(
        _("Is verified"),
        default=False,
        help_text=_("Whether the email has been verified"),
    )

    verification_token = models.CharField(
        _("Verification token"),
        max_length=100,
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

    # Status related
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

    # Timestamps
    created_at = models.DateTimeField(
        _("Created at"),
        auto_now_add=True,
        db_index=True,
    )

    updated_at = models.DateTimeField(
        _("Updated at"),
        auto_now=True,
    )

    class Meta:
        verbose_name = _("User Email")
        verbose_name_plural = _("User Emails")
        ordering = ["-is_primary", "-is_verified", "-created_at"]

        # Constraints
        constraints = [
            # User and email should be unique together
            models.UniqueConstraint(
                fields=["user", "email"],
                name="unique_user_email",
                violation_error_message=_("You have already added this email."),
            ),
            # Only one primary email per user
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

    def clean(self):
        """Model validation"""
        super().clean()

        # Normalize email
        self.email = self.email.lower().strip()

        # Validate email format
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email
        ):
            raise ValidationError({"email": _("Invalid email format.")})

        # Check if email is used by other users
        if self.is_active:
            existing = (
                Fnemail.objects.filter(email=self.email, is_active=True)
                .exclude(user=self.user)
                .first()
            )

            if existing:
                raise ValidationError(
                    {"email": _("This email is already used by another user.")}
                )

        # Validate primary email

        if self.is_primary and (not self.is_verified or not self.is_active):
            if (
                Fnemail.objects.filter(user=self.user)
                .exclude(pk=self.pk)
                .exists()
            ):

                raise ValidationError(
                    {
                        "is_primary": _(
                            "Only verified and active emails can be set as primary."
                        )
                    }
                )

    def save(self, *args, **kwargs):
        """Override save to sync with Fnuser.email"""
        self.full_clean()

        # If setting as primary, unset other primary emails
        if self.is_primary and self.pk:
            Fnemail.objects.filter(user=self.user, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)

        # Save the Fnemail instance

        # If this is primary and verified, sync to Fnuser.email
        if self.is_primary and self.is_verified and self.is_active:
            self.sync_to_user_email()

        # If this is the first email, set as primary
        if (
            not Fnemail.objects.filter(user=self.user)
            .exclude(pk=self.pk)
            .exists()
        ):
            self.is_primary = True
        super().save(*args, **kwargs)

    def sync_to_user_email(self):
        """
        Synchronize this email to the user's email field
        Only if this is the primary verified email
        """
        if self.is_primary and self.is_verified and self.is_active:
            if self.user.email != self.email:
                self.user.email = self.email
                self.user.save(update_fields=["email"])
                return True
        return False

    def generate_verification_token(self):
        """Generate verification token"""
        self.verification_token = uuid.uuid4().hex
        self.verification_sent_at = timezone.now()
        self.save(update_fields=["verification_token", "verification_sent_at"])
        return self.verification_token

    def verify(self, token):
        """Verify email with token"""
        if not self.verification_token or self.verification_token != token:
            return False

        # Check token expiration (7 days)
        if self.verification_sent_at:
            expiry_time = self.verification_sent_at + timezone.timedelta(days=7)
            if timezone.now() > expiry_time:
                return False

        self.is_verified = True
        self.verified_at = timezone.now()
        self.verification_token = None
        self.save(
            update_fields=["is_verified", "verified_at", "verification_token"]
        )

        # If this is user's first verified email, set as primary
        if not Fnemail.objects.filter(
            user=self.user, is_primary=True, is_verified=True
        ).exists():
            self.is_primary = True
            self.save(update_fields=["is_primary"])

        # Sync to user.email
        self.sync_to_user_email()

        return True

    def can_resend_verification(self):
        """Check if can resend verification email"""
        if not self.verification_sent_at:
            return True

        # Wait at least 60 seconds
        time_since_last = (
            timezone.now() - self.verification_sent_at
        ).total_seconds()
        return time_since_last >= 60

    def set_as_primary(self):
        """Set this email as primary"""
        if not self.is_verified:
            raise ValidationError(
                _("Email must be verified before setting as primary.")
            )

        if not self.is_active:
            raise ValidationError(_("Email must be active to set as primary."))

        # Unset other primary emails
        Fnemail.objects.filter(user=self.user, is_primary=True).update(
            is_primary=False
        )

        # Set this as primary
        self.is_primary = True
        self.save(update_fields=["is_primary"])

        # Sync to user.email
        self.sync_to_user_email()

        return True

    @property
    def status_display(self):
        """Display status text"""
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
        """Status badge color"""
        if not self.is_active:
            return "secondary"
        elif not self.is_verified:
            return "warning"
        elif self.is_primary:
            return "success"
        else:
            return "info"


# The end.
