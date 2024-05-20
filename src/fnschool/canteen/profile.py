import os
import sys
from pathlib import Path
import shutil
import tomllib

from fnschool import *
from fnschool.path import *
from fnschool.canteen import *
from fnschool.canteen.path import *
from fnschool.canteen.config import *


class Profile:
    def __init__(
        self, label=None, name=None, email=None, org_name=None, suppliers=None
    ):
        self._label = label
        self.name = name
        self.email = email
        self.org_name = org_name
        self.suppliers = suppliers
        self.fpath = Path(__file__).parent / "profile.toml"

    @property
    def label(self):
        label = self._label
        if " " in label:
            label = label.replace(" ", "")
        return label

    def get_profile(self):
        if not self.fpath.exists():
            with open(self.fpath, "w", encoding="utf-8") as f:
                f.write(
                    (
                        "\n"
                        + "profile = [\n"
                        + "    '{profile_label}',\n"
                        + "    '{operator_name}',\n"
                        + "    '{operator_email}',\n"
                        + "    '{organization_name}',\n"
                        + "    [\n"
                        + "        '{supplier_name_1}','{supplier_name_2}'\n"
                        + "    ]\n"
                        + "]\n"
                        + "# {the_end}"
                    ).format(
                        profile_label=_("Profile label"),
                        operator_name=_("Operator name"),
                        operator_email=_("Operator email"),
                        organization_name=_("Organization name or school name"),
                        supplier_name_1=_("Supplier name 1"),
                        supplier_name_2=_("Supplier name 2"),
                        the_end=_("The end."),
                    )
                )
            print_warning(_("Please update your profile file."))
            print_info(
                _(
                    "Profile label for data directory making, "
                    + "it shouldn't contain any space character.\n"
                    + "Supplier names are the supplier's alias."
                )
            )
            open_path(self.fpath)
            print_info(_("Ok! it was configured. (enter any key)"))
            input(">_ ")

        with open(self.fpath, "r", encoding="utf-8") as f:
            profile = tomllib.load(f)["profile"]
            profile = Profile(
                label=profile[0],
                name=profile[1],
                email=profile[2],
                org_name=profile[3],
                suppliers=profile[4],
            )
            return profile

        print_error(_("No profile information was got."))
        return None


# The end.
