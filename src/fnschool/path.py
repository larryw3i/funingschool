import os
import sys
from pathlib import Path, PosixPath
import shutil
import getpass
import platform
import subprocess

from appdirs import AppDirs
from fnschool.fnprint import *
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


# The end.
