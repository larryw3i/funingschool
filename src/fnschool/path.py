import os
import sys
from pathlib import Path
import shutil
import getpass
import platform
import subprocess

from appdirs import AppDirs
from fnschool.log import *

app_name = Path(__file__).parent.as_posix()
app_name = (
    app_name.split(os.sep)[-1]
    if os.sep in app_name
    else app_name.split("/")[-1]
)

app_author = "larryw3i"
user_name = getpass.getuser()

dirs = AppDirs(app_name, app_author)

app_dpath = Path(__file__).parent
data_dpath = app_dpath / "data"
config0_fpath = data_dpath / "config0.toml"
user_config_dir = Path(dirs.user_config_dir)
user_data_dir = Path(dirs.user_data_dir)
user0_data_dir = user_data_dir / user_name
config_fpath = user_config_dir / "config.toml"

for d in [
    user_config_dir,
    user_data_dir,
    user0_data_dir,
]:
    if not d.exists():
        os.makedirs(d)

if not config_fpath.exists():
    shutil.copy(config0_fpath, config_fpath)
    print_warning(
        _("Configuration file '%s' was copied to '%s'.")
        % (config0_fpath, config_fpath)
    )


def open_sys_explorer(dest=None):
    sys_platform = platform.platform()
    explorer_bin = (
        "explorer"
        if "Windows" in sys_platform
        else "open"
        if "macOS" in sys_platform
        else "nautilus"
    )
    dest = dest if Path(dest).exists() else Path.home()
    os.system(explorer_bin + " " + dest)


# The end.
