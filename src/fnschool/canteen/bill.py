import os
import sys
import calendar
from fnschool import *

from fnschool.canteen.spreadsheet.ctspreadsheet import *
from fnschool.canteen.operator import *
from fnschool.canteen.path import *


class Bill:
    def __init__(self):
        self._spreadsheet = None
        self._foods = None
        self._time_nodes = None
        self._operator_name = None
        self._food_classes = None
        self._operator = None

        pass

    @property
    def spreadsheet(self):
        if not self._spreadsheet:
            self._spreadsheet = CtSpreadSheet(self)
        return self._spreadsheet

    @property
    def foods(self):
        if not self._foods:
            self._foods = self.spreadsheet.purchasing.read_pfoods()
        return self._foods

    @property
    def purchaser(self):
        purchaser = self.foods[-1].purchaser
        return purchaser

    def make_spreadsheets(self):
        self.spreadsheet.update()
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
    def food_class_names(self):
        fclass_names = list(self.food_classes.keys())
        return fclass_names

    @property
    def food_classes(self):
        if not self._food_classes:
            print_info(_("Food classes files:"))
            for f in [
                self.operator.food_classes_fpath,
                food_classes_config0_fpath,
            ]:
                print("\t", f)
            with open(self.operator.food_classes_fpath, "rb") as f:
                self._food_classes = tomllib.load(f)
                print_info(
                    _(
                        'Your food classes were read from "{0}". '
                        + "It will be used first."
                    ).format(self.operator.food_classes_fpath)
                )

            food_classes0 = None
            with open(food_classes_config0_fpath, "rb") as f:
                food_classes0 = tomllib.load(f)
                print_info(
                    _('Preset food classes were read from "{0}".').format(
                        food_classes_config0_fpath
                    )
                )
            for fclass, name_likes in food_classes0.items():
                if fclass in self._food_classes.keys():
                    user_name_likes = self._food_classes.get(fclass)
                    for name_like in name_likes:
                        if not name_like in user_name_likes:
                            user_name_likes.append(name_like)
                    self._food_classes[fclass] = user_name_likes
                else:
                    self._food_classes[fclass] = name_likes

        return self._food_classes


    @property
    def operator(self):
        if not self._operator:
            self._operator = Operator(self)
        return self._operator


# The end.
