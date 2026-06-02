from django.conf import settings as SETTINGS
from fnschool.local import lang as lang_code


def settings(request):
    return {
        "AS_SITE": SETTINGS.AS_SITE,
        "AS_LOCAL": SETTINGS.AS_LOCAL,
        "LANGUAGE_CODE": lang_code
    }


# The end.
