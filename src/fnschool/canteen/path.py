import os
import sys
from fnschool import *
from fnschool.external import *


canteen_config0_fpath = Path(__file__).parent / "canteen.toml"
canteen_config_fpath = user_config_dir / "canteen.toml"
canteen_data_dpath = Path(__file__).parent / "data"
bill0_fpath = canteen_data_dpath / "bill.xlsx"
pre_consuming0_fpath = canteen_data_dpath / "consuming.xlsx"

if not canteen_config_fpath.exists():
    with open(canteen_config_fpath, "w", encoding="utf-8") as f:
        f.write(
            (
                "\n"
                + "profiles = [\n"
                + "    [\n"
                + "        '{profile_label}',\n"
                + "        '{operator_name}',\n"
                + "        '{operator_email}',\n"
                + "        '{organization_name}',\n"
                + "        [\n"
                + "            '{supplier_name_1}','{supplier_name_2}'\n"
                + "        ]\n"
                + "    ],\n"
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

    print_warning(_("Please update your configuration file."))
    open_file_via_app0(canteen_config_fpath)
    print_info(_("Ok! it was configured. (enter any key)"))
    input()

# The end.
