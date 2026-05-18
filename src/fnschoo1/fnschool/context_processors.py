from django.conf import settings as SETTINGS


def settings(request):
    return {
            "AS_SITE": SETTINGS.AS_SITE,
            "AS_LOCAL": SETTINGS.AS_LOCAL,
    }


# The end.
