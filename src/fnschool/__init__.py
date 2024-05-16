import os
import sys
import argparse
from pathlib import Path

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from fnschool.language import _
from fnschool.fnprint import *
from fnschool.path import *
from fnschool.entry import *
from fnschool.external import *

__version__ = "20240516.1949.11"


def print_app_name():
    app_name0 = [
        r" _____ _   _ ____   ____ _   _  ___   ___  _     ",
        r"|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    ",
        r"| |_  |  \| \___ \| |   | |_| | | | | | | | |    ",
        r"|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ ",
        r"|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|",
        r"",
    ]
    app_name0_len = max([len(l) for l in app_name0])
    version = "v" + __version__
    print("\n".join(app_name0))
    print(f"{version: >{app_name0_len}}")


# The end.
