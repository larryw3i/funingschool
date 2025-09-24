import os
import sys
import calendar
from fnschool import *
from fnschool.base import *

from fnschool.canteen.spreadsheet.spreadsheet_file import *
from fnschool.canteen.operator import *
from fnschool.canteen.path import *
from fnschool.canteen.currency import Currency
from fnschool.canteen.consuming import Consuming


class Bill(ClsBase):
    def __init__(self):
        super().__init__()
        self._spreadsheet = None
        self._foods = None
        self._time_nodes = None
        self._operator_name = None
        self._food_classes = None
        self._operator = None
        self._currency = None
        self._consuming = None
        self.significant_digits = 2
        self._meal_type = None

        pass

    @property
    def currency(self):
        if not self._currency:
            self._currency = Currency().get()
        return self._currency

    @property
    def consuming(self):
        if not self._consuming:
            self._consuming = Consuming(self)
        return self._consuming

    def get_CNY_chars(self, value):

        format_word = [
            "\u5206",  # fen1
            "\u89d2",  # jiao3
            "\u5143",  # yuan2
            "\u62fe",  # shi2
            "\u4f70",  # bai3
            "\u4edf",  # qian1
            "\u4e07",  # wan4
            "\u62fe",  # shi2
            "\u4f70",  # bai3
            "\u4edf",  # qian1
            "\u4ebf",  # yi4
            "\u62fe",  # shi2
            "\u4f70",  # bai3
            "\u4edf",  # qian1
            "\u4e07",  # wan4
            "\u62fe",  # shi2
            "\u4f70",  # bai3
            "\u4edf",  # qian1
            "\u5146",  # zhao4
        ]

        format_num = [
            "\u96f6",  # ling2
            "\u58f9",  # yi1
            "\u8d30",  # er4
            "\u53c1",  # san1
            "\u8086",  # si4
            "\u4f0d",  # wu3
            "\u9646",  # liu4
            "\u67d2",  # qi1
            "\u634c",  # ba1
            "\u7396",  # jiu3
        ]
        if type(value) == str:
            if "." in value:
                try:
                    value = float(value)
                except:
                    print_info(_("%s can't change.") % value)
            else:
                try:
                    value = int(value)
                except:
                    print_info(_("%s can't change.") % value)

        if type(value) == float:
            real_numbers = []
            for i in range(len(format_word) - 3, -3, -1):
                if value >= 10**i or i < 1:
                    real_numbers.append(int(round(value / (10**i), 2) % 10))

        elif isinstance(value, int):
            real_numbers = []
            for i in range(len(format_word), -3, -1):
                if value >= 10**i or i < 1:
                    real_numbers.append(int(round(value / (10**i), 2) % 10))

        else:
            print_info(_("%s can't change.") % value)

        zflag = 0
        start = len(real_numbers) - 3
        CNY_chars = []
        for i in range(start, -3, -1):
            if 0 < real_numbers[start - i] or len(CNY_chars) == 0:
                if zflag:
                    CNY_chars.append(format_num[0])
                    zflag = 0
                CNY_chars.append(format_num[real_numbers[start - i]])
                CNY_chars.append(format_word[i + 2])

            elif 0 == i or (0 == i % 4 and zflag < 3):
                CNY_chars.append(format_word[i + 2])
                zflag = 0
            else:
                zflag += 1

        if CNY_chars[-1] not in (
            format_word[0],
            # format_word[1]
        ):
            CNY_chars.append("\u6574") # zheng3.

        result = "".join(CNY_chars)
        return result

    @property
    def spreadsheet(self):
        if not self._spreadsheet:
            self._spreadsheet = SpreadsheetFile(self)
        return self._spreadsheet

    @property
    def foods(self):
        if not self._foods:
            self._foods = self.spreadsheet.purchasing.foods
        return self._foods

    def make_spreadsheets(self):
        self.spreadsheet.update()
        pass

    @property
    def food_classes(self):
        fclass_names = [
            _("Vegetables"),
            _("Meat"),
            _("Dairy and eggs, Pastries"),
            _("Grains"),
            _("Oils"),
            _("Condiments"),
            _("Fruits")

        ]
        return fclass_names

    
    @property
    def operator(self):
        if not self._operator:
            self._operator = Operator(self)
        return self._operator


# The end.
