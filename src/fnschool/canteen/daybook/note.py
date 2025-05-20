import os
import sys
import tkinter as tk
from tkinter import ttk

from fnschool import *
from fnschool.canteen.currency import *
from fnschool.canteen.daybook.noter import *
from fnschool.canteen.daybook.workbook import *
from fnschool.canteen.daybook.workbook.spreadsheet import *


class Note(ClsBase):
    def __init__(self):
        ClsBase.__init__(self)
        self.app.use_tk = True
        self.user = Noter(self)
        self._foods = None
        self._spreadsheet = None

        pass

    @property
    def foods(self):
        if not self._foods:
            purchase = self.spreadsheet.purchase
            self._foods = purchase.foods
            pass

        return self._foods
        pass

    @property
    def spreadsheet(self):
        if not self._spreadsheet:
            self._spreadsheet = SpreadSheet(self)
        return self._spreadsheet

    @property
    def file(self):
        return self._spreadsheet

    def gen(self):
        self.foods
        self.pre_exit()
        pass

    @property
    def currency(self):
        if not self._currency:
            self._currency = Currency().get()
        return self._currency
        pass


# The end.
