import getpass
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path, PosixPath

from platformdirs import *

from fnschool.app import *
from fnschool.tio import *

user_name = getpass.getuser()

dir_args = (app_name, app_author)

app_dpath = Path(__file__).parent
data_dpath = app_dpath / "data"
user_config_dir = Path(user_config_dir(*dir_args))
user_data_dir = Path(user_data_dir(*dir_args))
app_config_fpath = user_config_dir / "config.toml"

default_share_dpath = user_data_dir

for d in [
    user_config_dir,
    user_data_dir,
]:
    if not d.exists():
        os.makedirs(d)


def get_share_dpath(dpath):
    if str(app_dpath.as_posix()) in str(dpath.as_posix()):
        dpath = str((dpath).as_posix()).replace(
            (str(app_dpath.as_posix()) + "/"), ""
        )
        dpath = Path(dpath)

    dpath = default_share_dpath / dpath
    return dpath
    pass


def get_file_mtime(path):
    mtime = os.path.getmtime(path)
    mdatetime = datetime.fromtimestamp(mtime)
    return mdatetime


def get_file_ctime(path):
    ctime = os.path.getctime(path)
    cdatetime = datetime.fromtimestamp(ctime)
    return cdatetime


# The end.
