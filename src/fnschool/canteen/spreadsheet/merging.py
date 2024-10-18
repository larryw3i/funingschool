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
        self.last_fpath_dpath_key = _("last_bill_dpath")
        self.current_fpath_dpath_key = _("current_bill_dpath")
        self._last_wb = None
        self._current_wb = None
        pass
    
    @property
    def last_wb(self):
        if not self._last_wb:
            wb = load_workbook(self.last_fpath)
            self._last_wb = wb
        return self._last_wb

    @property
    def current_wb(self):
        if not self._current_wb:
            wb = load_workbook(self.current_fpath)
            self._current_wb = wb
        return self._current_wb

    @current_wb.setter
    def current_wb(self,wb):
        self._current_wb = wb
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
            self._last_fpath = fpath

        return self._last_fpath
        pass
    
    @property
    def current_fpath(self):
        if not self._current_fpath:
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

            self._current_fpath = fpath
        return self._current_fpath
        pass

    def get_food_sheet_names(self, wb):
        names = []
        for name in wb.sheetnames
            sheet = wb[sheet]
            if (
                sheet.cell(1,1).value 
                and self.food_sheet_title_like in str(sheet.cell(1,1).value)
            ):
                names.append(name)

        if self.food_sheet0_name in names:
            names.remove(self.food_sheet0_name)

        return names

    
    @current_fpath.setter
    def current_fpath(self, fpath):
        self._current_fpath = fpath
        pass

    

    def start(self):
        lwb = self.last_wb
        cwb = self.current_wb

        lwb_sheet_names = self.get_food_sheet_names(lwb)
        cwb_sheet_names = self.get_food_sheet_names(cwb)
        
        for name in lwb_sheet_names:
            if not name in cwb_sheet_names:
                pass 

        
    pass

# The end.
