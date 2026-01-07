import os
import sys
from pathlib import Path
import gettext
from helper.docs import _, project_dir, locale_dir, project_doc_dir, helper_dir


def write(lang=None):
    langs = (
        [lang] if lang else [p.name for p in locale_dir.iterdir() if p.is_dir()]
    )

    localedir = locale_dir
    localedir = localedir.as_posix()

    for l in langs:
        mo_file = locale_dir / l / "LC_MESSAGES" / "helper.mo"
        if mo_file.exists():
            t = gettext.translation(
                "helper", localedir, languages=[l], fallback=True
            )

            from helper.docs.readme import write

            write(l, t.gettext)
