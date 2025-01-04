import os
import sys
import subprocess
import tomllib

from helper.path import *


def sys_is_linux():
    return "inux" in sys.platform


def sys_is_win():
    return sys.platform.startswith("win")


def sys_is_darwin():
    return "darwin" in sys.platform


os_is_linux = sys_is_linux()
os_is_win = sys_is_win()
os_is_darwin = sys_is_darwin()


activate_fpath = (
    (venv_dpath / "Scripts" / "activate").as_posix()
    if os_is_win
    else (venv_dpath / "bin" / "activate").as_posix()
)

if not Path(activate_fpath).exists():
    sh_value = f"python3 -m venv {venv_dpath}"
    os.system(sh_value)
    print(_('Virtual Environment "{0}" has been made.').format(venv_dpath))


def sh(sh_value):
    sh_value = f". {activate_fpath}; " + sh_value
    os.system(sh_value)
    pass


# The end.
