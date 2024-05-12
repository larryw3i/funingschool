import os
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


class CtSpreadSheet:
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

    def save_workbook(self):
        bill_fpath0 = self.operator.bill_fpath_uuid
        print_error(
            _(
                "Do you want to save all updated data "
                + 'to "{0}"? or just save it as a '
                + 'copy to "{1}". (YyNn)'
            ).format(self.operator.bill_fpath, bill_fpath0)
        )
        print_warning(
            _(
                'If you save updated data to "{0}", '
                + "data of food sheets will be saved "
                + "for every month."
            ).format(self.operator.bill_fpath)
        )

        s_input = input(">_ ")

        print()
        print_info(_("Saving. . ."))

        if len(s_input) > 0 and s_input in "Yy":
            self.bwb.save(self.operator.bill_fpath)
            bill_fpath0 = sefl.operator.bill_fpath
            print_info(
                _(
                    "You can fill in the monthly missing data "
                    + "to food sheets, they will be saved "
                    + "for next updating."
                )
            )
        else:
            self.bwb.save(bill_fpath0)

        open_file(bill_fpath0)

        print_info(_("Updated data was saved."))

    def update(self):
        self.inventory.update()
        self.warehousing.update()
        self.unwarehousing.update()
        self.consuming.update()
        self.sfood.update()
        self.purchasingsum.update()
        self.consumingsum.update()
        self.cover.update()

        self.save_workbook()

        print_info(_("Update completely!"))


# The end.
