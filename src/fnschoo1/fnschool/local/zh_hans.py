import calendar
import io
import math
import os
import random
import re
import zipfile
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from django.utils import translation
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from fnschool.local.base import FnLocal


class FnZhHansLocal(FnLocal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def get_char_count(self, text):
        pattern = re.compile(r"[\u4e00-\u9fa5]")
        chinese_chars = pattern.findall(text)
        return len(chinese_chars)

    def get_monetary_amount(self, num):
        units = {
            "0": "\u96f6",  # ling2
            "1": "\u58f9",  # yi1
            "2": "\u8d30",  # er4
            "3": "\u53c1",  # san1
            "4": "\u8086",  # si4
            "5": "\u4f0d",  # wu3
            "6": "\u9646",  # liu4
            "7": "\u67d2",  # qi1
            "8": "\u634c",  # ba1
            "9": "\u7396",  # jiu3
        }

        levels = [
            "",
            "\u62fe",  # shi2
            "\u4f70",  # bai3
            "\u4edf",  # qian1
            "\u4e07",  # wan4
            "\u4ebf",  # yi4
            "\u5143",  # yuan2
            "\u89d2",  # jiao3
            "\u5206",  # fen1
            "\u6574",  # zheng3
        ]

        is_negative = False
        if num < 0:
            is_negative = True
            num = abs(num)
        if num == 0:
            return "\u96f6\u5143\u6574"  # ling2 yuan2 zheng3.

        num = Decimal(str(num)).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_UP
        )
        num_str = str(num)

        integer_part = None
        decimal_part = None
        if "." in num_str:
            integer_part, decimal_part = num_str.split(".")
        else:
            integer_part = num_str
            decimal_part = "00"

        result = []
        integer_part = integer_part.zfill(16)

        groups = [
            integer_part[-16:-12],
            integer_part[-12:-8],
            integer_part[-8:-4],
            integer_part[-4:],
        ]

        group_names = [
            "\u4e07",  # wan4
            "\u4ebf",  # yi4
            "\u4e07",  # wan4
            "\u5143",  # yuan2
        ]

        for i, group in enumerate(groups):
            group = group.lstrip("0")
            if not group:
                continue

            for j, digit in enumerate(group):
                if digit == "0":
                    if result and result[-1] != "\u96f6":  # \\u96f6 is ling2 .
                        result.append("\u96f6")  # \\u96f6 is ling2 .
                else:
                    result.append(units[digit])

                    if len(group) - j - 1 > 0:
                        result.append(levels[len(group) - j - 1])

            if group_names[i]:
                result.append(group_names[i])

        if decimal_part != "00":
            if decimal_part[0] != "0":
                result.append(units[decimal_part[0]])
                result.append("\u89d2")  # \\u89d2 is jiao3 .

            if decimal_part[1] != "0":
                result.append(units[decimal_part[1]])
                result.append("\u5206")  # \\u5206 is fen1 .
        else:
            result.append("\u6574")  # \\u6574 is zheng3 .

        output = "".join(result)

        output = re.sub("\u96f6+", "\u96f6", output)
        output = re.sub("\u96f6([\u4e07\u4ebf])", r"\1", output)
        output = re.sub("\u96f6\u5143", "\u5143", output)
        output = re.sub("\u96f6\u89d2\u96f6\u5206", "", output)
        output = re.sub("\u96f6\u5206", "", output)

        if output.startswith("\u58f9\u62fe"):
            output = output.replace("\u58f9\u62fe", "\u62fe", 1)

        if is_negative:
            output = "\u8d1f" + output

        return output


def get_local(*args, **kwargs):
    local = FnZhHansLocal(*args, **kwargs)
    return local


# The end.
