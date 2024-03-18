import os
import sys

from colorama import Fore, Style


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
