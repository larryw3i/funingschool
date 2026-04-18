import os
import sys
from pathlib import Path
import gettext
from datetime import datetime
from helper.docs import _, project_dir, locale_dir, project_doc_dir, helper_dir

project_change_log_dir = project_doc_dir / "CHANGELOG"
project_change_log_path = project_dir / "CHANGELOG.md"

_t_cp = _


class Release:
    def __init__(self,
        lang,
        _t,
        version=None,
        additions=None,
        changes=None,
        deprecations=None,
        fixes=None,
        removals=None,
    ):
        self.lang = lang
        self._t = _t
        self.version = version
        self.additions = additions or []
        self.changes = changes or []
        self.deprecations = deprecations or []
        self.fixes = fixes or []
        self.removals = removals or []
        self._date_of_release = None
        pass

    def date_of_release(self):
        if not self.version:
            return datetime.now()
        if self._date_of_release:
            return self._date_of_release
        dor = self.version.split(".")[0]
        dor = datetime.strptime(dor, "%Y%m%d")
        self._date_of_release = dor
        return self._date_of_release

    def get_markdown(self):
        _ = self._t
        l = self.lang
        dor = self.date_of_release()
        markdown = (
            _("## [{0}] - {1}-{2:0>2}-{3:0>2}").format(
                self.version or _("Unreleased"), dor.year, dor.month, dor.day
            )
            + "\n"
            + _("### Added")
            + "\n"
            + "\n".join([a for a in self.additions])
            + "\n"
            + _("### Changed")
            + "\n"
            + "\n".join([c for c in self.changes])
            + "\n"
            + _("### Deprecated")
            + "\n"
            + "\n".join([d for d in self.deprecations])
            + "\n"
            + _("### Fixed")
            + "\n"
            + "\n".join([f for f in self.fixes])
            + "\n"
            + _("### Removed")
            + "\n"
            + "\n".join([r for r in self.removals])
            + "\n"
        )
        return markdown


class Releases:
    def __init__(self, lang, _t):
        self.lang = lang
        self._t = _t
        pass

    def get_release_markdown(self, *args, **kwargs):
        release_markdown = Release(
            self.lang, self._t, *args, **kwargs
        ).get_markdown()
        return release_markdown
        pass

    def get_markdown(self):
        _ = self._t
        l = self.lang
        markdown = (
            "<hr/>"
            + "\n"
            + '<p align="center">'
            + '    <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/CHANGELOG/zh_CN.md">\u7b80\u4f53\u4e2d\u6587</a> \u2022'
            + '    <a href="https://github.com/larryw3i/funingschool/blob/master/Documentation/CHANGELOG/en_US.md">English</a>'
            + "</p>"
            + "\n"
            + "\n"
            + _("# Changelog")
            + "\n"
            + "\n"
            + self.get_release_markdown(
                additions=[
                    _(
                        "- Workbook File: Add properties to generated workbook file."
                    )
                ],
                changes=[
                    _(
                        "- Generate Wrokbook File: Add `timestamp` to generated file."
                    )
                ],
            )
            + self.get_release_markdown(
                version="20260415.80820.815",
                additions=[
                    _(
                        "- `Ingredient consumptions` Page: Make the Entry Fields in the table automatically scroll to the visible area when they are obscured by the header or the columns fixed on the left and one of them is inputted."
                    )
                ],
                changes=[
                    _(
                        "- Start Up: When starting up on a Linux distro, there may be a situation where the browser is already open but unable to access the specified URL. Therefore, it is advisable to delay opening the browser during startup."
                    ),
                ],
                fixes=[
                    _(
                        "- Edit Ingredient: Fixed issue the `Edit Ingredient` page be loaded with error if some `Category Name` is `None`."
                    )
                ],
            )
            + self.get_release_markdown(
                version="20260409.80155.835",
                changes=[
                    _(
                        "- `Ingredients List` Page: Make total price summary more intuitive."
                    )
                ],
                fixes=[
                    _(
                        "- Crate New Ingredients: Update the `new_ingredients` function, prevent adding too many meal types to the database when they are `empty`."
                    ),
                    _(
                        "- Ingredient Consumption: Fixed the error in displaying the ingredient progress bar on the ingredient consumption page."
                    ),
                ],
            )
            + self.get_release_markdown(
                version="20260127.80117.831",
                additions=[
                    _(
                        "- Add **CHANGELOG.md**: Add i18n feature for `CHANGELOG.md`."
                    ),
                    _(
                        "- Delete Ingredients: Add the function of batch deleting ingredients."
                    ),
                ],
                deprecations=[
                    _(
                        "- Patch `202511012053_copy_profiles_to_fnprofile`: This patch will be deprecated after February 2026."
                    )
                ],
            )
            + "\n"
        )
        return markdown

    def write(self):

        _ = self._t
        markdown = self.get_markdown()
        l = self.lang
        global _t_cp
        _ = _t_cp
        file_path = project_change_log_dir / (l + ".md")
        if not file_path.exists():
            file_path.touch()
            print(_('"{0}" has been created.').format(file_path))

        with open(file_path, "w", encoding="UTF-8") as file:
            file.write(markdown)
            print(_('"{0}" has been updated.').format(file_path))

        if l == "en_US":
            if not project_change_log_path.exists():
                project_change_log_path.touch()
                print(
                    _('"{0}" has been created.').format(project_change_log_path)
                )
            with open(project_change_log_path, "w", encoding="UTF-8") as file:
                file.write(markdown)
                print(
                    _('"{0}" has been updated.').format(project_change_log_path)
                )


def write(lang, _t):
    Releases(lang, _t).write()


_ = _t_cp

# The end.
