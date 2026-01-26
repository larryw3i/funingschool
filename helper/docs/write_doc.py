import os
import sys
from pathlib import Path
import gettext
import importlib
from helper.docs import _, project_dir, locale_dir, project_doc_dir, helper_dir


def write(lang=None):
    langs = (
        [lang] if lang else [p.name for p in locale_dir.iterdir() if p.is_dir()]
    )

    localedir = locale_dir
    localedir = localedir.as_posix()

    current_script = Path(__file__)
    current_dir = current_script.parent
    modules = [
        f.as_posix()
        .replace(project_dir.as_posix() + "/", "")
        .replace(".py", "")
        .replace("/", ".")
        for f in current_dir.glob("*.py")
        if f.name.startswith("write_") and not f.name == current_script.name
    ]

    for l in langs:
        mo_file = locale_dir / l / "LC_MESSAGES" / "helper.mo"
        if mo_file.exists():
            t = gettext.translation(
                "helper", localedir, languages=[l], fallback=True
            )
            for m in modules:
                m = importlib.import_module(m)
                if hasattr(m, "write"):
                    write_func = getattr(m, "write")
                    if callable(write_func):
                        write_func(l, t.gettext)
