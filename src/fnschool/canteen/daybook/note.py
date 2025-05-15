import os
import sys
import tkinter as tk
from tkinter import ttk

from fnschool import *
from fnschool.canteen.currency import *
from fnschool.canteen.daybook.operate.cover import *
from fnschool.canteen.daybook.operate.purchase import *
from fnschool.canteen.daybook.operate.consume import *
from fnschool.canteen.daybook.noter import *


class Note(ClsBase):
    def __init__(self):
        ClsBase.__init__(self)
        self.app.use_tk = True
        self.user = Noter(self)
        self._purchase = None
        self._pfoods = None
        pass

    @property
    def pfoods(self):
        if not self._pfoods:
            self._pfoods = self.purchase.pfoods
            pass

        return self._pfoods
        pass

    @property
    def purchase(self):
        if not self._purchase:
            self._purchase = Purchase(self)
        return self._purchase

    def gen(self):
        self.user.name
        self.pfoods

        self.pre_exit()
        pass

    @property
    def currency(self):
        if not self._currency:
            self._currency = Currency().get()
        return self._currency
        pass


# The end.
