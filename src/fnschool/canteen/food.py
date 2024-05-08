import os
import sys
from datetime import datetime

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
        is_abandoned=False,
        is_inventory=False,
    ):
        self.bill = bill
        self.name = name
        self.unit_name = unit_name
        self.count = float(count)
        self.total_price = float(total_price)
        xdate = (
            xdate.split("-")
            if "-" in xdate
            else (
                xdate.split(".")
                if "." in xdate
                else (
                    xdate.split("/")
                    if "/" in xdate
                    else [xdate[:4], xdate[4:6], xdate[6:]]
                )
            )
        )
        self.xdate = datetime(int(xdate[0]), int(xdate[1]), int(xdate[2]))
        self.purchaser = purchaser
        self.is_abandoned = is_abandoned
        self.is_inventory = is_inventory
        self.consumptions = []
        pass

    @property
    def unit_price(self):
        return self.total_price / self.count

    def get_remmainer(self,cdate):
        return self.count - sum(
            [
                c for d,c in self.consumptions
                if d < cdate
            ]
        ) if self.xdate < cdate else 0


# The end.
