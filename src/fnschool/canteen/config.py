import os
import sys
from pathlib import Path
import tomllib

from fnschool.canteen.path import *
from fnschool.log import *
from fnschool.external import *


class Config:
    def __init__(self, bill):
        self.bill = bill
        self.user_config = None
        self.app_config = None
        self.food_recounts_name = "food_recounts"
        self.food_unit_names_name = "food_unit_names"
        self.food_classes_name = "food_classes"

    def get_configs(self):
        if not self.user_cfg:
            with open(canteen_config_fpath, "rb") as f:
                self.user_cfg = tomllib.load(f) or {}
        if not self.app_config:
            with open(canteen_config0_fpath, "rb") as f:
                self.app_cfg = tomllib.load(f) or {}

        return (self.user_config, app_config)

    def get_configs(self, key):
        ucfg, acfg = self.get_configs()
        cfg = ucfg[key] + acfg[key]
        return None if cfg == [] else cfg

    def get_food_unit_names(self):
        return self.get_configs(self.food_unit_names_name)

    def get_food_recounts(self):
        return self.get_configs(self.food_recounts_name)

    def get_food_classes():
        return self.get_configs(self.food_classes_name)


# The end.
