import os
import sys
import tkinter as tk
from tkinter import ttk

from fnschool import *
from fnschool.canteen.noter import *
from fnschool.canteen.path import *
from fnschool.canteen.currency import *
from fnschool.canteen.forms.cover import Cover as CoverForm
from fnschool.canteen.forms.purchase import (
    Purchase as PurchaseForm,
    NonIgnorableGoodsSum as NonIgnorableGoodsSumForm,
    NonIgnorableGoods as NonIgnorableGoodsForm,
    IgnorableGoodsSum as IgnorableGoodsSumForm,
    IgnorableGoods as IgnorableGoodsForm,
)
from fnschool.canteen.forms.consumption import Consumption as ConsumptionForm
from fnschool.canteen.forms.good import Good as GoodForm
from fnschool.canteen.forms.goods import Goods as GoodsForm


class DayBook:
    def __init__(self):
        self._noter = None
        self._currency = None
        use_tk(yes=True)

        pass

    def gen(self):
        print(self.noter.name)
        pass

    @property
    def currency(self):
        if not self._currency:
            self._currency = Currency().get()
        return self._currency
        pass

    @property
    def noter(self):
        if not self._noter:
            self._noter = Noter( user_daybook_cfg_fpath)
        return self._noter
        pass


# The end.
