from django.conf import settings as SETTINGS


def settings(request):
    return {"EMAIL_BACKEND": SETTINGS.EMAIL_BACKEND}


# The end.
