import os
import sys
import gettext
import locale
from pathlib import Path

app_name = Path(__file__).parent.as_posix().split(os.sep)[-1]
locale_dir = (Path(__file__).parent / "locales").as_posix()


def get_language_code():
    locale.setlocale(locale.LC_ALL, "")
    language_code = locale.getlocale(locale.LC_MESSAGES)[0]
    app_language_codes = os.listdir(locale_dir)

    if language_code in app_language_codes:
        return language_code
    return "en_US"


translations = gettext.translation(
    app_name, locale_dir, fallback=True, languages=[get_language_code()]
)

T = translations.install()
t = T
_ = T
