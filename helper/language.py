import gettext
import locale
import os
import sys
from pathlib import Path

locale_dir = (Path(__file__).parent / "locales").as_posix()


def get_language_codes():
    lang_codes = os.listdir(locale_dir)
    lang_codes = [
        l for l in lang_codes if (Path(locale_dir) / l / "LC_MESSAGES").is_dir()
    ]
    return lang_codes


def get_language_code():
    locale.setlocale(locale.LC_ALL, "")
    language_code = (
        locale.getdefaultlocale()[0]
        if sys.platform.startswith("win")
        else locale.getlocale()[0]
    )
    app_language_codes = get_language_codes()

    language_code = (
        language_code if language_code in app_language_codes else "en_US"
    )

    return language_code


app_language_code = get_language_code()

language_code_is_zh_CN = "zh_CN" in app_language_code
is_zh_CN = language_code_is_zh_CN
t_domain = Path(__file__).parent.name

T = gettext.translation(
    t_domain, locale_dir, fallback=True, languages=[app_language_code]
)
T.install()

t = T.gettext
_ = t

# The end.
