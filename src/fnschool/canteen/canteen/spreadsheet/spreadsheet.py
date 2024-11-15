import os
import random
import sys
from pathlib import Path
import shutil
import calendar
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

from tkinter import filedialog

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *
from fnschool.canteen.spreadsheet.purchasing import Purchasing
from fnschool.canteen.spreadsheet.consuming import Consuming
from fnschool.canteen.spreadsheet.preconsuming import PreConsuming
from fnschool.canteen.spreadsheet.inventory import Inventory
from fnschool.canteen.spreadsheet.warehousing import Warehousing
from fnschool.canteen.spreadsheet.unwarehousing import Unwarehousing
from fnschool.canteen.spreadsheet.unwarehousingsum import UnwarehousingSum
from fnschool.canteen.spreadsheet.food import Food as SFood
from fnschool.canteen.spreadsheet.purchasingsum import PurchasingSum
from fnschool.canteen.spreadsheet.consumingsum import ConsumingSum
from fnschool.canteen.spreadsheet.cover import Cover
from fnschool.canteen.spreadsheet.merging import Merging


class SpreadSheet:
    def __init__(self, bill):
        self.bill = bill
        self.operator = self.bill.operator
        self._bill_fpath = None
        self._purchasing_fpath = None
        self._bwb = None
        self._pwb = None
        self._preconsuming = None
        self._purchasing = None
        self._consuming = None
        self._inventory = None
        self._warehousing = None
        self._unwareshousing = None
        self._purchasingsum = None
        self._consumingsum = None
        self._sfood = None
        self._cover = None
        self.sd = self.bill.significant_digits

        self.preconsuming_name0 = "出库计划表"
        self.purchasing_name = None
        self.consuming_name = "出库单"
        self.inventory_name = "食材盘存表"
        self.warehousing_name = "入库单"
        self.unwarehousing_name = "未入库明细表"
        self.purchasingsum_name = "入库、未入库汇总表"
        self.consumingsum_name = "出库汇总表"
        self.sfood_name = "材料台账母表"
        self.cover_name = "六大类总封面"

    @property
    def bill_fpath(self):
        if not self._bill_fpath:
            self._bill_fpath = self.bill.operator.bill_fpath
        return self._bill_fpath

    @property
    def bill_workbook(self):
        if not self._bwb:
            self._bwb = load_workbook(self.bill_fpath)
            print_info(
                _('Spreadsheet "{0}" is in use.').format(self.bill_fpath)
            )
        return self._bwb

    @property
    def bwb(self):
        return self.bill_workbook

    def del_bill_workbook(self):
        self._bwb = None
        self._bill_fpath = None

    def del_bwb(self):
        self.del_bill_workbook()

    @property
    def consumingsum(self):
        if not self._consumingsum:
            self._consumingsum = ConsumingSum(self.bill)
        return self._consumingsum

    @property
    def purchasingsum(self):
        if not self._purchasingsum:
            self._purchasingsum = PurchasingSum(self.bill)
        return self._purchasingsum

    @property
    def sfood(self):
        if not self._sfood:
            self._sfood = SFood(self.bill)
        return self._sfood

    @property
    def unwarehousing(self):
        if not self._unwareshousing:
            self._unwareshousing = Unwarehousing(self.bill)
        return self._unwareshousing

    @property
    def cover(self):
        if not self._cover:
            self._cover = Cover(self.bill)

        return self._cover

    @property
    def warehousing(self):
        if not self._warehousing:
            self._warehousing = Warehousing(self.bill)
        return self._warehousing

    @property
    def purchasing(self):
        if not self._purchasing:
            self._purchasing = Purchasing(self.bill)
        return self._purchasing

    @property
    def preconsuming(self):
        if not self._preconsuming:
            self._preconsuming = PreConsuming(self.bill)
        return self._preconsuming

    @property
    def consuming(self):
        if not self._consuming:
            self._consuming = Consuming(self.bill)
        return self._consuming

    @property
    def inventory(self):
        if not self._inventory:
            self._inventory = Inventory(self.bill)
        return self._inventory

    @property
    def meal_type(self):
        return self.bill.meal_type

    def save_workbook(self):
        bill_fpath0 = self.operator.bill_fpath_uuid
        print_error(
            _(
                "Do you want to save all updated data "
                + 'to "{0}"? or just save it as a '
                + 'copy to "{1}". (Yy[N]n)'
            ).format(self.operator.bill_fpath, bill_fpath0)
        )
        print_warning(
            _(
                'If you save updated data to "{0}", '
                + "data of food sheets will be saved "
                + "for every month."
            ).format(self.operator.bill_fpath)
        )

        s_input = input0()

        print()
        print_info(_("Saving. . ."))

        if len(s_input) > 0 and s_input in "Yy":
            self.bwb.save(self.operator.bill_fpath)
            bill_fpath0 = self.operator.bill_fpath
            print_info(
                _(
                    "You can fill in the monthly missing data "
                    + "to food sheets, they will be saved "
                    + "for next updating."
                )
            )
        else:
            self.bwb.save(bill_fpath0)

        print_info(
            _('Updated data has been saved to "{0}".').format(bill_fpath0)
        )

        open_path(bill_fpath0)

        print_info(_("Updated data was saved."))

    def print_summary(self, foods=None):
        bfoods = foods or self.bill.foods
        cfoods = [f for f in bfoods if not f.is_abandoned]
        currency_mark = self.bill.currency.mark
        summary = []
        summary_len = 0

        inventory_mm1 = sum([f.total_price for f in cfoods if f.is_inventory])
        inventory_mm1 = round(inventory_mm1, self.sd + 1)

        inventory_mm1 = (
            _("Inventory of last month: ") + currency_mark + str(inventory_mm1)
        )

        warehousing_m = sum(
            [f.total_price for f in cfoods if not f.is_inventory]
        )

        warehousing_m_cp = warehousing_m
        warehousing_m = (
            _("Warehousing of this month: ")
            + currency_mark
            + str(warehousing_m)
        )
        inventory_mm1_warehousing_m = (
            _("Total: ")
            + currency_mark
            + str(round(sum([f.total_price for f in cfoods]), 2))
        )
        consuming_m = 0
        for f in cfoods:
            f_consuming_m = sum([c for __, c in f.consumptions])
            consuming_m += f_consuming_m * f.unit_price
        consuming_m = round(consuming_m, self.sd + 1)

        consuming_m_cp = consuming_m
        consuming_m = (
            _("Consuming of this month: ") + currency_mark + str(consuming_m)
        )

        month_day_m1 = sorted([f.xdate for f in cfoods])[0]
        for f in cfoods:
            month_day_m1 = max([d for d, __ in f.consumptions] + [month_day_m1])

        inventory_m = sum(
            [
                f.get_remainder(month_day_m1) * f.unit_price
                for f in cfoods
                if f.get_remainder(month_day_m1) > 0
            ]
        )
        inventory_m = round(inventory_m, self.sd + 1)

        inventory_m_cp = inventory_m
        inventory_m = (
            _("Inventory of this month: ") + currency_mark + str(inventory_m)
        )

        consuming_m_inventory_m = (
            _("Total: ")
            + currency_mark
            + str(round(consuming_m_cp + inventory_m_cp, self.sd + 1))
        )

        afoods = [f for f in bfoods if f.is_abandoned]
        unwarehousing_m = (
            _("Unwarehousing of this month: ")
            + currency_mark
            + str(sum([f.total_price for f in afoods]))
        )

        total_purchasing_m = (
            _("Total purchasing of this month: ")
            + currency_mark
            + str(
                round(
                    sum([f.total_price for f in bfoods if not f.is_inventory]),
                    self.sd + 1,
                )
            )
        )
        summary = [
            inventory_mm1,
            warehousing_m,
            inventory_mm1_warehousing_m,
            consuming_m,
            inventory_m,
            consuming_m_inventory_m,
            warehousing_m,
            unwarehousing_m,
            total_purchasing_m,
        ]

        summary_len = max(
            [len(s) + len([c for c in s if is_zh_CN_char(c)]) for s in summary]
        )
        summary_sep = get_random_sep_char() * summary_len
        consuming_date_m1 = (
            f"{self.bill.consuming.year}"
            + f".{self.bill.consuming.month:0>2}"
            + f".{self.bill.consuming.day_m1:0>2}"
        )
        summary = (
            [summary_sep]
            + [self.meal_type]
            + [summary_sep]
            + summary[:3]
            + [summary_sep]
            + summary[3:6]
            + [summary_sep]
            + summary[6:]
            + [summary_sep]
            + [f"{consuming_date_m1:>{summary_len}}"]
        )
        summary = "\n".join(summary)
        print()
        print_error(_("Summary:"))
        print_info(summary)
        print()

    def del_sheets_var(self):
        self._inventory = None
        self._warehousing = None
        self._unwareshousing = None
        self._consuming = None
        self._sfood = None
        self._purchasingsum = None
        self._consumingsum = None
        self._cover = None

    def merge(self):
        merging = Merging(self.bill)
        merging.start()
        pass

    def update(self):

        foods0 = self.bill.foods.copy()
        meal_types = list(set([f.meal_type for f in foods0]))

        for t in meal_types:

            print_info(_("Updating sheets for {0}.").format(t))

            _foods = [f for f in foods0 if f.meal_type == t]

            del self.bill.meal_type
            self.bill.foods = _foods

            self.inventory.update()
            self.warehousing.update()
            self.unwarehousing.update()
            self.consuming.update()
            self.sfood.update()
            self.purchasingsum.update()
            self.consumingsum.update()
            self.cover.update()

            self.print_summary()

            self.save_workbook()

            self.del_sheets_var()
            self.del_bwb()

        print_info(_("Update completely!"))


# The end.
