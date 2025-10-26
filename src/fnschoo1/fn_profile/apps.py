from django.apps import AppConfig


class FnUserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fn_profile"

    def ready(self):
        import fn_profile.signals


# The end.
