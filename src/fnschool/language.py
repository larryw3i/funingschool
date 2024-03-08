import os
import sys
import gettext
import locale
from pathlib import Path

app_name = Path(__file__).parent.as_posix().split(os.sep)[-1]
locale_dir = (Path(__file__).parent / 'locales').as_posix()

translations = gettext.translation(
    app_name, 
    locale_dir, 
    fallback=True, 
    languages=[
        language_code
    ]
)

T = translations.install()
t = T
_ = T
