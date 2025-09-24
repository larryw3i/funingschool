from django.db import models
from fnschool import *
from django.utils.translation import gettext as _

# Create your models here.

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name=_("Phone Number")
    )
    affiliation = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Affiliation")
    )

    superior_department = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Superior department"),
    )

    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name=_("Date of Birth")
    )

    address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name=_("Address")
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name=_("Avatar")
    )

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return _("{0}'s Profile").format(self.user.username)


# The end.
