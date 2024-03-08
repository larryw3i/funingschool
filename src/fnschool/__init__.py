import ps
import sys
from pathlib import Path
import shutil

from appdirs import AppDirs


from fnschool.language import T, t, _

__version__ = "2024.0308"

app_name = "fnschool"
app_author = "larryw3i"
dirs = AppDirs(app_name,app_author)

app_dpath = Path(__file__).parent
data_dpath = app_path / "data"
config0_fpath = data_path / "config0.toml"
config_fpath = Path(dirs.user_config_dir) / 'config.toml'

if not config_fpath.exists():
    shutil.copy(config0_fpath,config_fpath)
    print(
        _("Configuration file '%s' was copied to '%s'.") % (
            config0_fpath,
            config_fpath
        )
    )










