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
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
        if not self.username:
            raise ValidationError(
                _(
                    "The username may not be empty. Please enter a valid username."
                )
            )

        super().save(*args, **kwargs)

    def get_email(self):
        try:
            primary_email = self.emails.get(
                is_primary=True, is_active=True, is_verified=True
            )
            return primary_email.email
        except FnEmail.DoesNotExist:
            verified_email = self.emails.filter(
                is_verified=True, is_active=True
            ).first()
            if verified_email:
                return verified_email.email
            return None

    def get_primary_email(self):
        try:
            return self.emails.get(is_primary=True, is_active=True)
        except FnEmail.DoesNotExist:
            return None

    def has_verified_email(self):
        return self.emails.filter(is_verified=True, is_active=True).exists()

    def get_verified_emails(self):
        return self.emails.filter(is_verified=True, is_active=True)

    def get_all_emails(self):
        return self.emails.filter(is_active=True)

    def email_exists(self, email):
        return self.emails.filter(email=email, is_active=True).exists()

    def can_add_email(self):
        max_emails = max_email_count
        return self.emails.filter(is_active=True).count() < max_emails

    @property
    def email_count(self):
        return self.emails.filter(is_active=True).count()

    @property
    def verified_email_count(self):
        return self.emails.filter(is_verified=True, is_active=True).count()


class FnEmail(models.Model):

    user = models.ForeignKey(
        Fnuser,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name=_("User"),
        db_index=True,
    )

    email = models.EmailField(
        _("Email Address"),
        max_length=256,
        db_index=True,
        help_text=_("Please enter a valid email address."),
    )

    # 验证相关
    is_verified = models.BooleanField(
        _("Is Verified"),
        default=False,
        help_text=_("Has the email been verified."),
    )

    verification_token = models.CharField(
        _("Verification Token"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Token used for email verification."),
    )

    verification_sent_at = models.DateTimeField(
        _("Last verification email sent time"),
        blank=True,
        null=True,
        help_text=_("The last time a verification email was sent."),
    )

    verified_at = models.DateTimeField(
        _("Verified at"),
        blank=True,
        null=True,
        help_text=_("The time when email verification was passed."),
    )

    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Is this email address active?"),
    )

    is_primary = models.BooleanField(
        _("Is Primary"),
        default=False,
        help_text=_("Is it used as the primary email?"),
    )

    created_at = models.DateTimeField(
        _("Added at"),
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
                    "There can only be one primary email."
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
        super().clean()
        self.email = self.email.lower().strip()
        if not re.match(
            r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.email
        ):
            raise ValidationError(
                {"email": _("The email format is incorrect.")}
            )

        if self.is_active:
            existing = (
                FnEmail.objects.filter(email=self.email, is_active=True)
                .exclude(user=self.user)
                .first()
            )

            if existing:
                raise ValidationError(
                    {"email": _("This email has been used by another user.")}
                )

        if self.is_primary and (not self.is_verified or not self.is_active):
            raise ValidationError(
                {
                    "is_primary": _(
                        "Only verified and enabled email addresses can be set as primary email addresses."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.is_primary and self.pk:
            FnEmail.objects.filter(user=self.user, is_primary=True).exclude(
                pk=self.pk
            ).update(is_primary=False)

        super().save(*args, **kwargs)

        if (
            not FnEmail.objects.filter(user=self.user)
            .exclude(pk=self.pk)
            .exists()
        ):
            self.is_primary = True
            self.save(update_fields=["is_primary"])

    def generate_verification_token(self):
        self.verification_token = uuid.uuid4().hex
        self.verification_sent_at = timezone.now()
        self.save(update_fields=["verification_token", "verification_sent_at"])
        return self.verification_token

    def verify(self, token):
        if not self.verification_token or self.verification_token != token:
            return False

        if self.verification_sent_at:
            expiry_time = self.verification_sent_at + timezone.timedelta(
                days=(resend_verification_email_time_interval + 1 * 60)
            )
            if timezone.now() > expiry_time:
                return False

        self.is_verified = True
        self.verified_at = timezone.now()
        self.verification_token = None
        self.save(
            update_fields=["is_verified", "verified_at", "verification_token"]
        )

        if not FnEmail.objects.filter(
            user=self.user, is_primary=True, is_active=True
        ).exists():
            self.is_primary = True
            self.save(update_fields=["is_primary"])

        return True

    def can_resend_verification(self):
        if not self.verification_sent_at:
            return True

        time_since_last = (
            timezone.now() - self.verification_sent_at
        ).total_seconds()
        return time_since_last >= resend_verification_email_time_interval

    def disable(self):
        if self.is_primary:
            raise ValidationError(_("The primary email cannot be disabled."))

        self.is_active = False
        self.save(update_fields=["is_active"])

    def enable(self):
        self.is_active = True
        self.save(update_fields=["is_active"])

    def set_as_primary(self):
        if not self.is_verified:
            raise ValidationError(
                _(
                    "The email has not been verified, and cannot be set as the primary email."
                )
            )

        if not self.is_active:
            raise ValidationError(
                _(
                    "The email has been disabled and cannot be set as the primary email."
                )
            )

        FnEmail.objects.filter(user=self.user, is_primary=True).update(
            is_primary=False
        )

        self.is_primary = True
        self.save(update_fields=["is_primary"])

    def resend_verification(self):
        if not self.can_resend_verification():
            raise ValidationError(
                _(
                    "Please wait for {time_interval} seconds and then resend"
                ).format(time_interval=resend_verification_email_time_interval)
            )

        self.generate_verification_token()
        return True

    @property
    def status_display(self):
        if not self.is_active:
            return _("Disabled")
        elif not self.is_verified:
            return _("verified")
        elif self.is_primary:
            return _("Primary")
        else:
            return _("Enabled")

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

    @property
    def age_days(self):
        return (timezone.now() - self.created_at).days


# The end.
