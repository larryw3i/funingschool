import os
import sys
import platform
import math
import random

from colorama import Fore, Style

if platform.system() == "Windows":
    from colorama import just_fix_windows_console

    just_fix_windows_console()


def get_random_sep_char():
    sep_char = random.choice(
        ["-", "+", "=", "|", "o", "`", ".", "x", "z", "#", "^", "*"]
    )
    return sep_char


def is_zh_CN_char(value):
    result = (
        0x4E00 <= ord(value) <= 0x9FA5
        or 0xFF00 <= ord(value) <= 0xFFEF
        or 0x3000 <= ord(value) <= 0x303F
    )
    return result


def input0():
    i_value = input(">_ ")
    return i_value


def get_len(value):
    value_len = 0
    if isinstance(value, str):
        value_len = len(value) + len([c for c in value if is_zh_CN_char(c)])
    else:
        value_len = len(value)
    return value_len


def get_zh_CN_chars_len(value):
    value_len = len([c for c in value if is_zh_CN_char(c)])
    return value_len


def sqr_slist(slist):
    if not isinstance(slist, list):
        return slist

    slist_len = len(slist)
    slist_len_sqrt = math.ceil(slist_len**0.5)

    slist_col_count = slist_len_sqrt
    for col_index in range(0, slist_col_count):
        col_values = [
            (i, slist[i])
            for i in range(0, slist_len)
            if i % slist_col_count == col_index
        ]

        rc_len = max([get_len(v) for i, v in col_values]) + 1
        for i, v in col_values:
            v_len = rc_len - get_zh_CN_chars_len(v)
            slist[i] = f"{v:<{v_len}}"

    s_value = ""
    for i, v in enumerate(slist):
        if i % slist_col_count == 0 and i != 0:
            s_value += "\n"
        s_value += v

    return s_value


def print_info(*args, **kwargs):
    print(Fore.GREEN, end="")
    print(*args, **kwargs, end="")
    print(Style.RESET_ALL)


def print_warning(*args, **kwargs):
    print(Fore.YELLOW, end="")
    print(*args, **kwargs, end="")
    print(Style.RESET_ALL)


def print_error(*args, **kwargs):
    print(Fore.RED, end="")
    print(*args, **kwargs, end="")
    print(Style.RESET_ALL)


# The end.
