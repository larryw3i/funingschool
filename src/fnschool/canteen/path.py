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
user_documents_dpath = Path.home() / "Documents"
operator_name_fpath = user_config_dir / "operator_name.txt"



if not operator_name_fpath.exists():
    with open(operator_name_fpath, "w", encoding="utf-8") as f:
        f.write("")


def get_food_classes_config_fpath(user_name):
    fpath = user_config_dir / user_name / "food_classes.toml"

    if not fpath.exists():
        shutil.copy(food_classes_config0_fpath, fpath)


# The end.
