from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import FnUser


@receiver(post_save, sender=User)
def create_user_fn_profile(sender, instance, created, **kwargs):
    if created:
        FnUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_fn_profile(sender, instance, **kwargs):
    if hasattr(instance, "fn_profile"):
        instance.fn_profile.save()


# The end.
