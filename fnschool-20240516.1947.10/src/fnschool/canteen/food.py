import os
import sys
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from fnschool import *


class Food:
    def __init__(
        self,
        bill,
        name,
        unit_name,
        count,
        total_price,
        xdate,
        purchaser,
        fclass,
        is_abandoned=False,
        is_inventory=False,
    ):
        self.bill = bill
        self.name = name
        self.unit_name = unit_name
        self.count = float(count)
        self.fclass = fclass
        self.total_price = float(total_price)
        self.xdate = self.datefstr(xdate)
        self.purchaser = purchaser
        self.is_abandoned = is_abandoned
        self.is_inventory = is_inventory
        self.consumptions = []
        pass

    def datefstr(self, value):
        value = (
            value.split("-")
            if "-" in value
            else (
                value.split(".")
                if "." in value
                else (
                    value.split("/")
                    if "/" in value
                    else [value[:4], value[4:6], value[6:]]
                )
            )
        )
        value = datetime(int(value[0]), int(value[1]), int(value[2]))
        return value

    @property
    def unit_price(self):
        return self.total_price / self.count

    def get_remainder(self, cdate):
        if self.xdate < cdate:
            return self.count - sum(
                [c for d, c in self.consumptions if d <= cdate]
            )
        if self.xdate == cdate:
            return self.count
        if self.xdate > cdate:
            return 0


# The end.
