import os
import sys
import tkinter as tk
from tkinter import ttk

from fnschool import *
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


class Note(ClsBase):
    def __init__(self):
        use_tk(True)
        ClsBase.__init__(self)
        pass

    def gen(self):
        print(self.user.name)
        self.cfg.save() 
        pass

    @property
    def currency(self):
        if not self._currency:
            self._currency = Currency().get()
        return self._currency
        pass


# The end.
