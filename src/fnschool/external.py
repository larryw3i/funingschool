import os
import sys
import subprocess

from fnschool.language import *
from fnschool.log import *
from fnschool.path import *


def sys_is_linux():
    return "inux" in sys.platform


def sys_is_win():
    return sys.platform.startswith("win")


def sys_is_darwin():
    return "darwin" in sys.platform


def get_new_issue_url():
    return (
        "https://gitee.com/larryw3i/funingschool/issues"
        if language_code_is_zh_CN
        else "https://github.com/larryw3i/funingschool/issues/new"
    )


def open_file_via_app0(file_path):
    file_path = str(file_path)
    bin_name = (
        "xdg-open"
        if sys_is_linux()
        else "open"
        if sys_is_darwin()
        else "start"
    )
    os.system(bin_name + " " + file_path)


# The end.
