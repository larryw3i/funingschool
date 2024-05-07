import os
import sys

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
    ):
        self.bill = bill
        self.name = name
        self.unit_name = unit_name
        self.count = count
        self.total_price = total_price
        self.xdate = xdate
        self.purchaser = purchaser
        pass


    @property
    def unit_price(self):
        return self.total_price / self.count

# The end.
