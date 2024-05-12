import os
import sys
import calendar
from fnschool import *

from fnschool.canteen.spreadsheet.ctspreadsheet import *
from fnschool.canteen.operator import *
from fnschool.canteen.path import *


class Bill:
    def __init__(self):
        self._spreadsheet = None
        self._foods = None
        self._time_nodes = None
        self._operator_name = None
        self._food_classes = None
        self._operator = None

        print_app_name()
        pass

    def get_CNY_chars(self, value):
        format_word = [
            "分",
            "角",
            "元",
            "拾",
            "佰",
            "仟",
            "万",
            "拾",
            "佰",
            "仟",
            "亿",
            "拾",
            "佰",
            "仟",
            "万",
            "拾",
            "佰",
            "仟",
            "兆",
        ]

        format_num = [
            "零",
            "壹",
            "贰",
            "叁",
            "肆",
            "伍",
            "陆",
            "柒",
            "捌",
            "玖",
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

        if CNY_chars[-1] not in (format_word[0], format_word[1]):
            CNY_chars.append("整")

        result = "".join(CNY_chars)
        return result

    @property
    def spreadsheet(self):
        if not self._spreadsheet:
            self._spreadsheet = CtSpreadSheet(self)
        return self._spreadsheet

    @property
    def foods(self):
        if not self._foods:
            self._foods = self.spreadsheet.purchasing.read_pfoods()
        return self._foods

    @property
    def purchaser(self):
        purchaser = self.foods[-1].purchaser
        return purchaser

    def make_spreadsheets(self):
        self.spreadsheet.update()
        print_info(
            _(
                "If you feel {0} is great, "
                + "please sponsor it. "
                + "Your sponsorship will keep "
                + "the project alive."
            ).format(app_name)
        )
        print_warning("\t" + _("Sponsor URL: {0}").format(get_sponsor_url()))
        pass

    @property
    def time_nodes(self):
        if not self._time_nodes:
            year = self.foods[-1].xdate.year
            month = self.foods[-1].xdate.month
            self._time_nodes = sorted(
                list(
                    set(
                        [f.xdate for f in self.foods]
                        + [
                            datetime(
                                year,
                                month,
                                calendar.monthrange(year, month)[1],
                            )
                        ]
                    )
                )
            )

        return self._time_nodes

    @property
    def food_class_names(self):
        fclass_names = list(self.food_classes.keys())
        return fclass_names

    @property
    def food_classes(self):
        if not self._food_classes:
            print_info(_("Food classes files:"))
            for f in [
                self.operator.food_classes_fpath,
                food_classes_config0_fpath,
            ]:
                print("\t", f)
            with open(self.operator.food_classes_fpath, "rb") as f:
                self._food_classes = tomllib.load(f)
                print_info(
                    _(
                        'Your food classes were read from "{0}". '
                        + "It will be used first."
                    ).format(self.operator.food_classes_fpath)
                )

            food_classes0 = None
            with open(food_classes_config0_fpath, "rb") as f:
                food_classes0 = tomllib.load(f)
                print_info(
                    _('Preset food classes were read from "{0}".').format(
                        food_classes_config0_fpath
                    )
                )
            for fclass, name_likes in food_classes0.items():
                if fclass in self._food_classes.keys():
                    user_name_likes = self._food_classes.get(fclass)
                    for name_like in name_likes:
                        if not name_like in user_name_likes:
                            user_name_likes.append(name_like)
                    self._food_classes[fclass] = user_name_likes
                else:
                    self._food_classes[fclass] = name_likes

        return self._food_classes

    @property
    def operator(self):
        if not self._operator:
            self._operator = Operator(self)
        return self._operator


# The end.
