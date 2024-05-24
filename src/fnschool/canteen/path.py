import os
import sys
import tomllib
import shutil
from fnschool import *
from fnschool.external import *


food_classes_config0_fpath = Path(__file__).parent / "food_classes.toml"
canteen_data_dpath = Path(__file__).parent / "data"
bill0_fpath = canteen_data_dpath / "bill.xlsx"
pre_consuming0_fpath = canteen_data_dpath / "consuming.xlsx"
operator_name_fpath = user_config_dir / (_("operator_name") + ".txt")

user_canteen_dpath = user_data_dir / _("canteen")


if not operator_name_fpath.exists():
    with open(operator_name_fpath, "w", encoding="utf-8") as f:
        f.write("")


# The end.
