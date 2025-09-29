from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from fnschool import *

# Create your models here.


class Profile(AbstractUser):
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
    bio = models.TextField(
        max_length=512, blank=True, verbose_name=_("Biography")
    )

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

    def __str__(self):
        return _("{0}'s Profile").format(self.username)


# The end.
