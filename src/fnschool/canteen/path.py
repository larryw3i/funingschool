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
canteen_links_dpath = user_documents_dpath / "fnschool" / "canteen"
operator_name_fpath = user_config_dir / "operator_name.txt"

operator_name_link_fpath = canteen_links_dpath / "operator_name.txt"
food_classes_config_link_fpath = canteen_links_dpath / "canteen.toml"


if not canteen_links_dpath.exists():
    os.makedirs(canteen_links_dpath, exist_ok=True)

if not operator_name_fpath.exists():
    with open(operator_name_fpath, "w", encoding="utf-8") as f:
        f.write("")
    os.link(operator_name_fpath.as_posix(), operator_name_link_fpath.as_posix())


def get_food_classes_config_fpath(user_name):
    fpath = user_config_dir / user_name / "food_classes.toml"

    if not fpath.exists():
        shutil.copy(food_classes_config0_fpath, fpath)
        make_link(fpath.as_posix(), food_classes_config_link_fpath.as_posix())


# The end.
