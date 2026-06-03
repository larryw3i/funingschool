from django.conf import settings as SETTINGS


def settings(request):
    return {
        "AS_SITE": SETTINGS.AS_SITE,
        "AS_LOCAL": SETTINGS.AS_LOCAL,
        "USER_FULL_NAME": (
            request.user.get_full_name(request)
            if request.user.is_authenticated
            else None
        ),
    }


# The end.
