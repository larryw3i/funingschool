import os
import sys
import argparse
from pathlib import Path

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from fnschool.language import _
from fnschool.log import *
from fnschool.path import *
from fnschool.entry import *
from fnschool.external import *

__version__ = "20240412.2301.19"


# The end.
