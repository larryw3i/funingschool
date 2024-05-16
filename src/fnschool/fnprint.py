import os
import sys
import platform

from colorama import Fore, Style

if platform.system() == "Windows":
    from colorama import just_fix_windows_console

    just_fix_windows_console()


def is_zh_CN_char(value):
    result = (
        0x4E00 <= ord(value) <= 0x9FA5
        or 0xFF00 <= ord(value) <= 0xFFEF
        or 0x3000 <= ord(value) <= 0x303F
    )
    return result


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
