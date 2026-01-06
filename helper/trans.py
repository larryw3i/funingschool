import gettext
import os
from pathlib import Path

localedir = Path(__file__).parent / "locale"
localedir = localedir.as_posix()

lang = os.getenv("LANGUAGE", "en_US")
t = gettext.translation("helper", localedir, languages=[lang], fallback=True)
_ = t.gettext

# The end.
