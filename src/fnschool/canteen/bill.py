import os
import sys
import calendar
from fnschool import *

from fnschool.canteen.spreadsheet import *
from fnschool.canteen.path import *


class Bill:
    def __init__(self):
        self._spreadsheet = None
        self._foods = None
        self._time_nodes = None
        self._operator_name = None
        self._food_classes = None

        pass

    @property
    def spreadsheet(self):
        if not self._spreadsheet:
            self._spreadsheet = SpreadSheet(self)
        return self._spreadsheet

    @property
    def foods(self):
        if not self._foods:
            self._foods = self.spreadsheet.read_foods()
        return self._foods

    def make_spreadsheets(self):
        for f in self.foods:
            print(f.xdate, f.name, f.count, f.total_price, f.unit_price)
        print(self.time_nodes)
        pass

    @property
    def time_nodes(self):
        if not self._time_nodes:
            year = self.foods[-1].xdate.year
            month = self.foods[-1].xdate.month
            self._time_nodes = sorted(
                list(
                    set(
                        [f.xdate for f in self.foods]
                        + [
                            datetime(
                                year,
                                month,
                                calendar.monthrange(year, month)[1],
                            )
                        ]
                    )
                )
            )

        return self._time_nodes

    @property
    def food_classes(self):
        if not self._food_classes:
            config_fpath = get_food_classes_config_fpath(self.operator_name)
            with open(config_fpath, "r", encoding="utf-8") as f:
                self._food_classes = tomllib.load(f)

        return self._food_classes

    @property
    def operator_name(self):
        if not self._operator_name:
            with open(operator_name_fpath, "r", encoding="utf-8") as f:
                self._operator_name = f.read()
            if self._operator_name == "":
                print_info(_("Tell me your name please:"))
                self._operator_name = input(">_ ")
                with open(operator_name_fpath, "w", encoding="utf-8") as f:
                    f.write(self._operator_name)
        return self._operator_name

    @property
    def operator_dpath(self):
        dpath = user_config_dir / self.operator_name
        if not dpath.exists():
            os.makedirs(dpath,exist_ok=True)
        return dpath

    @property
    def operator_consuming_dpath(self):
        dpath = self.operator_dpath / "consuming"
        if not dpath.exists():
            os.makedirs(dpath, exist_ok = True)
        return dpath


# The end.
