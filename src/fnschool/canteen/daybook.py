import os
import sys

from fnschool import *
from fnschool.operator import *
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
        self._operator = None
        self._currency = None
        pass

    def gen(self):
        pass

    @property
    def currency(self):
        if not self._currency:
            self._currency = Currency().get()
        return self._currency
        pass

    @property
    def operator(self):
        if not self._operator:
            self._operator = Operator(self)
        return self._operator
        pass


# The end.
