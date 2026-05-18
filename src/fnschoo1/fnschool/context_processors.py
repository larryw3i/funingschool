from django.conf import settings as SETTINGS


def settings(request):
    return {"EMAIL_HOST": SETTINGS.EMAIL_HOST}


# The end.
