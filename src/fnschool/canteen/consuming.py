import os
import sys
from datetime import datetime
from fnschool import *


class Consuming:
    def __init__(self, bill):
        self.bill = bill
        self._year = None
        self._month = None
        self._day_m1 = None
        

    @property
    def year(self):
        if not self._year:
            foods = self.bill.foods
            foods = sorted(foods, key=lambda f: f.xdate)
            self._year = foods[-1].xdate.year
        return self._year

    @property
    def month(self):
        if not self._month:
            foods = self.bill.foods
            foods = sorted(foods, key=lambda f: f.xdate)
            self._month = foods[-1].xdate.month
        return self._month

    @property
    def date_m1(self):
        date_m1 = datetime(
            self.year,
            self.month,
            self.day_m1
        )
        return date_m1

    @property
    def day_m1(self):
        if not self._day_m1:
            self._day_m1 = 0
            foods = self.bill.foods
            for f in foods:
                self._day_m1 = max(
                    [d.day for d, __ in f.consumptions] + [self._day_m1]
                )
            if self._day_m1 < 1:
                print_error(
                    _(
                        "It seems you didn't design the consumption, "
                        + "please restart {0} and design "
                        + "the consumptions"
                    ).format(app_name)
                )
                exit()
        return self._day_m1
