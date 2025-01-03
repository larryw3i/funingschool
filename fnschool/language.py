import os
import sys
import gettext
import locale
from pathlib import Path
from fnschool.app import *

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


app_language_code = get_language_code()

language_code_is_zh_CN = "zh_CN" in app_language_code
is_zh_CN = language_code_is_zh_CN

T = gettext.translation(
    app_name, locale_dir, fallback=True, languages=[app_language_code]
)
T.install()

t = T.gettext
_ = t

# The end.
