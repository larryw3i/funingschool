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
        self._count_threshold = None
        pass

    @property
    def get_remainder_total_price_c(self, cdate):
        remainder = get_remainder(cdate)
        consuming_count = self.get_consuming_count(cdate)

        unit_price_l, unit_price_m, count_threshold = self.count_threshold

        total_price = (
            (
                (count_threshold - consuming_count) * unit_price_m
                + (self.count - count_threshold) * unit_price_l
            )
            if consuming_count <= count_threshold
            else remainder * unit_price_l
        )

        return total_price

    @property
    def get_unit_price_c(self, cdate):
        if not self.bill.disable_infinite_decimal:
            return self.unit_price

        unit_price_l, unit_price_m, count_threshold = self.count_threshold

        consuming_count = self.get_consuming_count(cdate)
        unit_price_c = (
            unit_price_m if consuming_count <= count_threshold else unit_price_l
        )

        return unit_price_c

    @property
    def count_threshold(self):
        if not self._count_threshold:

            sd = self.bill.significant_digits or 2
            total_price = self.total_price
            count = self.count

            dot_0_r = r"[.|0]+$"
            count_s = str(count)
            count_s = re.sub(dot_0_r, "", count_s)
            count_sd = len(count_s.split(".")[1]) if "." in count_s else 0
            count_scale = 10**count_sd

            total_price_s = str(total_price)
            total_price_s = re.sub(dot_0_r, "", total_price_s)
            total_price_sd = (
                len(total_price_s.split(".")[1]) if "." in total_price_s else 0
            )

            sd = max(sd, count_sd, total_price_sd)
            scale = 10**sd

            unit_price = total_price / count
            total_price0 = int(total_price * scale)
            count0 = int(count * scale)

            unit_price_sd = sd - count_sd
            unit_price_scale = 10**unit_price_sd
            unit_price0 = (
                math.floor((total_price0 / count0) * unit_price_scale)
                / unit_price_scale
            )

            total_price1 = unit_price0 * count
            total_price1 = (
                int(total_price1)
                if re.search(dot_0_r, str(total_price1))
                else total_price1
            )

            count1 = count0 / scale
            count1 = int(count1) if re.search(dot_0_r, str(count1)) else count1
            count1_s = str(count1)
            count1_sd = len(count1_s.split(".")[1]) if "." in count1_s else 0

            count2 = count1
            if count1_sd > 0:
                count2 = math.floor(count1 * 10**count1_sd)

            unit_price1 = unit_price0
            unit_price1 = (
                int(unit_price1)
                if re.search(dot_0_r, str(unit_price1))
                else unit_price1
            )

            total_price_diff = round(total_price - total_price1, sd + 1)
            total_price_d_s = str(total_price_diff)
            total_price_d_sd = (
                len(total_price_d_s.split(".")[1])
                if "." in total_price_d_s
                else 0
            )

            total_price_diff2 = total_price_diff
            total_price_diff2_p = 1 / (10**total_price_d_sd)
            if total_price_diff2 > 0.0:
                total_price_diff2 = math.floor(
                    total_price_diff * 10**total_price_d_sd
                )

            count2_len2 = len(str(count2)) + 1

            unit_price3 = round(unit_price1 / 10**count1_sd, sd + 1)
            unit_price4 = round(unit_price3 + total_price_diff2_p, sd + 1)
            count_threshold = round(total_price_diff2 / count_scale, sd + 1)

            self._count_threshold = (unit_price3, unit_price4, count_threshold)
        return self._count_threshold

    def datefstr(self, value):
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            if "'" in value:
                value = value.replace("'", "")
            if "=" in value:
                value = value.replace("=", "")

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
        return 0 if not self.count else (self.total_price / self.count)

    def get_remainder(self, cdate):
        if self.xdate < cdate:
            return self.count - sum(
                [c for d, c in self.consumptions if d <= cdate]
            )
        if self.xdate == cdate:
            return self.count
        if self.xdate > cdate:
            return 0

    def get_consuming_count(self, cdate):
        consuming_count = self.count - self.get_remainder(cdate)
        return consuming_count


# The end.
