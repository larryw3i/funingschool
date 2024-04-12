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


os_is_linux = sys_is_linux()
os_is_win = sys_is_win()
os_is_darwin = sys_is_darwin()


def get_new_issue_url():
    return (
        "https://gitee.com/larryw3i/funingschool/issues"
        if language_code_is_zh_CN
        else "https://github.com/larryw3i/funingschool/issues/new"
    )


def open_file_via_app0(file_path):
    file_path = str(file_path)
    bin_name = "open" if (sys_is_linux() or sys_is_darwin()) else "start"
    if sys_is_win():
        if file_path.endswith(".toml"):
            bin_name = "notepad"
    else:
        file_path = "'" + file_path + "'"

    _sh = f"{bin_name} {file_path}"
    os.system(_sh)


# The end.
