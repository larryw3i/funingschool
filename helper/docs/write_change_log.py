import os
import sys
from pathlib import Path
import gettext
from datetime import datetime
from helper.docs import _, project_dir, locale_dir, project_doc_dir, helper_dir

project_change_log_dir = project_doc_dir / "CHANGELOG"
project_change_log_path = project_dir / "CHANGELOG.md"

__cp = _


def write(lang, _t):
    _ = _t
    l = lang
    date_now = datetime.now()
    change_log = [
        "<hr/>",
        "",
        _("# Changelog"),
        "",
        _("## [{0}] - {1}-{2:0>2}-{3:0>2}").format(
            "Unreleased", date_now.year, date_now.month, date_now.day
        ),
        "",
        _("### Added"),
        "",
        _("### Changed"),
        "",
        _("### Deprecated"),
        "",
        _("### Fixed"),
        "",
        _("### Removed"),
        "",
        _("## [{0}] - {1}-{2}-{3}").format(
            "20260127.80117.831", "2026", "01", "27"
        ),
        "",
        _("### Added"),
        _("- Add **CHANGELOG.md**: Add i18n feature for `CHANGELOG.md`."),
        _(
            "- Delete Ingredients: Add the function of batch deleting ingredients."
        ),
        "",
        _("### Changed"),
        "",
        _("### Deprecated"),
        _(
            "- Patch `202511012053_copy_profiles_to_fnprofile`: This patch will be deprecated after February 2026."
        ),
        "",
        _("### Fixed"),
        "",
        _("### Removed"),
    ]
    change_log = "\n".join(change_log)

    _ = __cp
    file_path = project_change_log_dir / (l + ".md")
    if not file_path.exists():
        file_path.touch()
        print(_('"{0}" has been created.').format(file_path))

    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(change_log)
        print(_('"{0}" has been updated.').format(file_path))

    if l == "en_US":
        if not project_change_log_path.exists():
            project_change_log_path.touch()
            print(_('"{0}" has been created.').format(project_change_log_path))
        with open(project_change_log_path, "w", encoding="UTF-8") as file:
            file.write(change_log)
            print(_('"{0}" has been updated.').format(project_change_log_path))


_ = __cp

# The end.
