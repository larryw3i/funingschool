import os
import sys
from pathlib import Path
import tomllib

from fnschool.canteen.path import *
from fnschool.log import *
from fnschool.external import *


def get_food_recounts_config():
    cfg = None
    with open(canteen_config_fpath, "rb") as f:
        cfg = tomllib.load(f).get("canteen", {}).get("recounts", [])
    if cfg == []:
        print_error(
            _("'recounts' hasn't been configured yet. configure it now?(YyNn)")
        )
        if input() in "Yy":
            open_file_via_app0(canteen_config0_fpath)
            open_file_via_app0(canteen_config_fpath)
            return get_food_recounts_config()

    return None if cfg == [] else cfg
