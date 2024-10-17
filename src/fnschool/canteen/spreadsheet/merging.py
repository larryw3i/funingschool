import os
import random
import sys
from pathlib import Path
import shutil
import calendar
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

import tkinter as tk
from tkinter import filedialog, ttk

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *

class Merging( Base ):
    def __init__(self,bill):
        super.__init__(bill)
        self._last_fpath = None
        self._current_fpath = None
        self.last_fpath_dpath_key = _("last_bill_dir_path")
        self.current_fpath_dpath_key = _("current_bill_dir_dpath")
        pass


    @property
    def last_fpath(self):
        if not self._last_fpath:
            root = tk.Tk()
            conf_initialdir = self.config.get(self.last_fpath_dpath_key)
            conf_initialdir = Path(conf_initialdir) if conf_initialdir else None
            initialdir = (
                conf_initialdir
                or documents_dpath 
                or Path.home()
            )
            fpath = filedialog.askopenfile(
                root,
                title = _("Select the last bill spreadsheet"),
                initialdir = initialdir,
                filetypes = self.filetypes_xlsx,
            )
        pass

    @property
    def current_fpath(self):
            root = tk.Tk()
            conf_initialdir = self.config.get(self.last_fpath_dpath_key)
            conf_initialdir = Path(conf_initialdir) if conf_initialdir else None
            initialdir = (
                conf_initialdir
                or documents_dpath 
                or Path.home()
            )
            fpath = filedialog.askopenfile(
                root,
                title = _("Select the last bill spreadsheet"),
                initialdir = initialdir,
                filetypes = self.filetypes_xlsx,
            )

        pass
    
    

    pass

# The end.
