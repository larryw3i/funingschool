import os
import sys
from pathlib import Path, PosixPath
import shutil
import getpass
import platform
import subprocess
from datetime import datetime

from appdirs import AppDirs
from fnschool.print import *
from fnschool.app import *


user_name = getpass.getuser()

dirs = AppDirs(app_name, app_author)

app_dpath = Path(__file__).parent
data_dpath = app_dpath / "data"
user_config_dir = Path(dirs.user_config_dir)
user_data_dir = Path(dirs.user_data_dir)


for d in [
    user_config_dir,
    user_data_dir,
]:
    if not d.exists():
        os.makedirs(d)


def get_file_mtime(path):
    mtime = os.path.getmtime(path)
    mdatetime = datetime.fromtimestamp(mtime)
    return mdatetime


def get_file_ctime(path):
    ctime = os.path.getctime(path)
    cdatetime = datetime.fromtimestamp(ctime)
    return cdatetime


# The end.
