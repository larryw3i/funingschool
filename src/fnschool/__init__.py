import os
import sys
import argparse
import random
from pathlib import Path
import tomllib
import re
import math
import copy
from datetime import datetime, timedelta
from tkinter import filedialog, ttk
import tkinter as tk

import calendar
from datetime import datetime

import pandas as pd
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import numbers
from openpyxl.styles import Font
from fnschool.app import *
from fnschool.language import _
from fnschool.print import *
from fnschool.path import *
from fnschool.entry import *
from fnschool.external import *
from fnschool.user import *
from fnschool.config import *


__version__ = "20241118.81142.858"


# The end.
