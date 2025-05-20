import os
import sys

from fnschool.canteen.daybook.workbook import *


class Food:
    def __init__(self):
        self._counting_date = None
        self._meal_type = None
        self._name = None
        self._quantity = None
        self._total_price = None
        self._residual = None
        self._negligible = None
        self._consumptions = []
        pass

    @property
    def counting_date(self):
        return self._counting_date

    @counting_date.setter
    def counting_date(self, value):
        self._counting_date = value

    @property
    def meal_type(self):
        return self._meal_type

    @meal_type.setter
    def meal_type(self, value):
        self._meal_type = value

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def total_price(self):
        return self._total_price

    @total_price.setter
    def total_price(self, value):
        self._total_price = value

    @property
    def residual(self):
        return self._residual

    @residual.setter
    def residual(self, value):
        self._residual = value

    @property
    def negligible(self):
        return self._negligible

    @negligible.setter
    def negligible(self, value):
        return self._negligible

    @property
    def consumptions(self):
        return self._consumptions


# The end.
