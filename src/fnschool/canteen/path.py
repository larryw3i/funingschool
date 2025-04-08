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
user_canteen_dpath = user_data_dir / _("canteen")
operator_name_fpath = user_canteen_dpath / (_("operator_name") + ".txt")
documents_dpath = Path.home() / "Documents"

user_daybook_dpath = user_canteen_dpath / _("daybook")
noter_name_fpath = user_canteen_dpath / (_("noter_name") + ".txt")

for d in [
    user_canteen_dpath,
]:
    if not d.exists():
        os.makedirs(d, exist_ok=True)

for f in [operator_name_fpath, noter_name_fpath]:
    if not f.exists():
        with open(f, "w", encoding="utf-8") as _f:
            _f.write("")


# The end.
