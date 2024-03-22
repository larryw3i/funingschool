import os
import sys
from pathlib import Path
import tomllib

from fnschool.canteen.path import *
from fnschool.log import *
from fnschool.external import *


def get_food_unit_names_config():
    cfg = None
    with open(canteen_config_fpath, "rb") as f:
        cfg = tomllib.load(f).get("canteen", {}).get("unit_names", [])
    with open(canteen_config0_fpath, "rb") as f:
        cfg = cfg + tomllib.load(f).get("canteen", {}).get("unit_names", [])
    return get_food_recounts_config()

    return None if cfg == [] else cfg


def get_food_recounts_config():
    cfg = None
    with open(canteen_config_fpath, "rb") as f:
        cfg = tomllib.load(f).get("canteen", {}).get("recounts", [])
    with open(canteen_config0_fpath, "rb") as f:
        cfg = cfg + tomllib.load(f).get("canteen", {}).get("recounts", [])

    return None if cfg == [] else cfg
