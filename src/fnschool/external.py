import os
import sys
import subprocess

from fnschool.language import *
from fnschool.fnprint import *
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
        if is_zh_CN
        else "https://github.com/larryw3i/funingschool/issues/new"
    )


def get_sponsor_url():
    return (
        (
            "https://gitee.com/larryw3i/funingschool"
            + "/blob/master/Documentation/"
            + "README.zh_CN.md#%E8%B5%9E%E5%8A%A9"
        )
        if is_zh_CN
        else ("https://github.com/larryw3i/" + "funingschool#support")
    )


def open_path(file_path):
    file_path = str(file_path)
    bin_name = "open" if (sys_is_linux() or sys_is_darwin()) else "start"
    file_path = '"' + file_path + '"'
    if sys_is_win():
        if file_path.endswith('.toml"'):
            bin_name = "notepad"
        elif Path(file_path).isdir():
            bin_name = 'explorer'
        else:
            os.startfile(file_path)

            return None

    os.system(f"{bin_name} {file_path}")

    return None


# The end.
