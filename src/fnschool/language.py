import os
import sys
import gettext
import locale
from pathlib import Path

app_name = Path(__file__).parent.as_posix()
app_name = (
    app_name.split(os.sep)[-1]
    if os.sep in app_name
    else app_name.split("/")[-1]
)
locale_dir = (Path(__file__).parent / "locales").as_posix()


def get_language_code():
    locale.setlocale(locale.LC_ALL, "")
    language_code = (
        locale.getdefaultlocale()[0]
        if sys.platform.startswith("win")
        else locale.getlocale()[0]
    )
    app_language_codes = os.listdir(locale_dir)

    language_code = (
        language_code if language_code in app_language_codes else "en_US"
    )

    return language_code


translations = gettext.translation(
    app_name, locale_dir, fallback=True, languages=[get_language_code()]
)


T = translations.install()
t = T
_ = T
