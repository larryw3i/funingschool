import os
import sys
from fnschool import *


friends0_fpath = Path(__file__).parent / "canteen.toml"
friends_fpath = user_config_dir / "canteen.toml"
canteen_data_dpath = Path(__file__).parent / "data"
workbook0_fpath = canteen_data_dpath / "workbook0.xlsx"

if not friends_fpath.exists():
    shutil.copy(friends0_fpath,friends_fpath)
    print_info(
        _("Configuration file '%s' was copied to '%s'.") % (
            friends0_fpath, friends_fpath
        )
    )
    print_warning(
        _("Please update your configuration file.")
    )
    print_info(
        _("Ok! it was configured. (enter any key)")
    )
    input()


