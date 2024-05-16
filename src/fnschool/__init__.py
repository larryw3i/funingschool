import os
import sys
import argparse
import random
from pathlib import Path

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from fnschool.language import _
from fnschool.fnprint import *
from fnschool.path import *
from fnschool.entry import *
from fnschool.external import *

__version__ = "20240517.0037.59"


def print_app_name():
    app_name0 = [
        r" _____ _   _ ____   ____ _   _  ___   ___  _     ",
        r"|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    ",
        r"| |_  |  \| \___ \| |   | |_| | | | | | | | |    ",
        r"|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ ",
        r"|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|",
        r"",
    ]
    app_name1 = [
        r"|`````````````````````````````````````````````````|",
        r"| _____ _   _ ____   ____ _   _  ___   ___  _     |",
        r"||  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    |",
        r"|| |_  |  \| \___ \| |   | |_| | | | | | | | |    |",
        r"||  _| | |\  |___) | |___|  _  | |_| | |_| | |___ |",
        r"||_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____||",
        r"|                                                 |",
        r'```````````````````````````````````````````````````',
        r"",
    ]

    app_name0_0 = "\n".join(app_name0)
    app_name1_1 = '\n'.join(app_name1)
    app_name = random.choice([app_name0_0,app_name1_1])

    app_name_len = max([len(l) for l in app_name.split('\n')])
    version0 = "v" + __version__
    version0_0 = f"{version0:>{app_name_len}}"
    version0_1 = f"{version0:^{app_name_len}}"

    version = random.choice([version0_0,version0_1])
    p_app_name = (
        '\n'
        + app_name
        + version
        + '\n'
    )
    print(p_app_name)


# The end.
