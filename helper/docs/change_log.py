import os
import sys
from pathlib import Path
import gettext
from helper.docs import _, project_dir, locale_dir, project_doc_dir, helper_dir

project_change_log_dir = project_doc_dir / "CHANGELOG"
project_change_log_path = project_dir / "CHANGELOG.md"

__cp = _


def write(lang, _t):
    _ = _t
    l = lang
    change_log = [
        "<hr/>",
        "",
        _("# Changelog"),
        "",
        _("## [{0}] - {1}-{2}-{3}").format("Unreleased", "2026", "01", "22"),
        "",
        _("### Added"),
        _("- **Add CHANGELOG.md**: Add i18n feature for `CHANGELOG.md`."),
        "",
        _("### Changed"),
        "",
        _("### Deprecated"),
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
