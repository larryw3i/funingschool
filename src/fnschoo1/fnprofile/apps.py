from django.apps import AppConfig


class FnUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fnprofile"

    def ready(self):
        import fnprofile.signals


# The end.
