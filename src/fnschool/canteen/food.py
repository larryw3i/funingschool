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
        meal_type=None,
        is_abandoned=False,
        is_inventory=False,
    ):
        self.bill = bill
        self.sd = self.bill.significant_digits
        self.name = name
        self.unit_name = unit_name
        self.count = round(float(count), self.sd + 1)
        self.fclass = fclass
        self.total_price = round(float(total_price), self.sd + 1)
        self.xdate = self.datefstr(xdate)
        self.purchaser = purchaser
        self.is_abandoned = is_abandoned
        self.is_inventory = is_inventory
        self.consumptions = []
        self.meal_type = meal_type or ""
        self._count_threshold = None
        pass

    def get_display_name(self, is_residual=False, time_node0=None):
        name = self.name + (
            _("({0})").format(
                (
                    (_("Remaining") + "|")
                    if (is_residual or (time_node0 and self.xdate < time_node0))
                    else ""
                )
                + (self.meal_type if self.meal_type else "")
            )
        )

        return name

    @property
    def count_threshold(self):
        if not self.count:
            print_error(
                _('The count of "{0}" is 0, you need to delete it maybe.')
            )
            return [0, 0, 0]

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
            count1_scale = 10**count1_sd

            count2 = count1
            if count1_sd > 0:
                count2 = math.floor(count1 * count1_scale)

            unit_price1 = unit_price0
            unit_price1 = (
                int(unit_price1)
                if re.search(dot_0_r, str(unit_price1))
                else unit_price1
            )

            total_price_diff = round(total_price - total_price1, sd + 1)

            if not total_price_diff:
                self._count_threshold = (self.unit_price, self.unit_price, 0)
            else:
                total_price_d_s = str(total_price_diff)

                total_price_d_sd = (
                    len(total_price_d_s.split(".")[1])
                    if "." in total_price_d_s
                    else 0
                )

                total_price_diff2 = total_price_diff
                total_price_diff2_scale = 10 ** (total_price_d_sd - count_sd)
                total_price_diff2_p = 1 / (total_price_diff2_scale)
                if total_price_diff2 > 0.0:
                    total_price_diff2 = math.floor(
                        total_price_diff * 10**total_price_d_sd
                    )
                unit_price3_scale = 10 ** (count1_sd - count_sd)
                unit_price3 = round(unit_price1 / unit_price3_scale, sd + 1)

                unit_price4 = round(unit_price3 + total_price_diff2_p, sd + 1)
                count_threshold = round(total_price_diff2 / count_scale, sd + 1)

                self._count_threshold = (
                    unit_price3,
                    unit_price4,
                    count_threshold,
                )

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
        value = 0 if not self.count else (self.total_price / self.count)
        value = round(value, self.sd + 1)
        return value

    def get_remainder(self, cdate):
        value = None
        if self.xdate < cdate:
            value = self.count - sum(
                [c for d, c in self.consumptions if d <= cdate]
            )
        if self.xdate == cdate:
            value = self.count
        if self.xdate > cdate:
            value = 0
        value = round(value, self.sd + 1)
        return value

    def get_consuming_count(self, cdate):
        consuming_count = self.count - self.get_remainder(cdate)
        consuming_count = round(consuming_count, self.sd + 1)
        return consuming_count


# The end.
