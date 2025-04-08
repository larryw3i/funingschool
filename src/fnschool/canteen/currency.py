import os
import sys
from abc import *

from fnschool import *


class CurrencyBase:
    def __init__(self, name=None, unit=None, mark=None):
        self.name = name
        self.unit = unit
        self.mark = mark

    @abstractmethod
    def locale(self):
        pass


class Currency_CNY(CurrencyBase):
    def __init__(self, name="CNY", unit=_("CNY"), mark="\u00a5"):
        super().__init__(name, unit, mark)

    def locale(self, value):
        format_char = [
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
        nan_error_msg = _("%s is NOT a NUMBER.") % value

        if type(value) == str:
            if not value.replace(".", "").isnumeric():
                print_error(nan_error_msg)

        real_numbers = []
        if type(value) == float:
            for i in range(len(format_char) - 3, -3, -1):
                if value >= 10**i or i < 1:
                    real_numbers.append(int(round(value / (10**i), 2) % 10))

        elif isinstance(value, int):
            for i in range(len(format_char), -3, -1):
                if value >= 10**i or i < 1:
                    real_numbers.append(int(round(value / (10**i), 2) % 10))
        else:
            pass

        zflag = 0
        start = len(real_numbers) - 3
        CNY_chars = []
        for i in range(start, -3, -1):
            if 0 < real_numbers[start - i] or len(CNY_chars) == 0:
                if zflag:
                    CNY_chars.append(format_num[0])
                    zflag = 0
                CNY_chars.append(format_num[real_numbers[start - i]])
                CNY_chars.append(format_char[i + 2])

            elif 0 == i or (0 == i % 4 and zflag < 3):
                CNY_chars.append(format_char[i + 2])
                zflag = 0
            else:
                zflag += 1

        if CNY_chars[-1] not in (
            format_char[0],
            # format_char[1]
        ):
            CNY_chars.append("整")

        result = "".join(CNY_chars)
        return result


class Currency:
    def __init__(self):
        pass

    def get(self):
        return Currency_CNY() if is_zh_CN else Currency_CNY()

    pass


# The end.
