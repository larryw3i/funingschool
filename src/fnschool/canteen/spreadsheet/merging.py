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

    def get_sheet(self, name=None, wb=None):
        sheet = None
        wb = wb or self.bwb

        if name in wb.sheetnames:
            sheet = wb[name]
        else:
            sheet = wb.copy_worksheet(wb[self.sheet_name])
            sheet.title = name

        for row_index in range(1, sheet.max_row + 1):
            rc1_value = sheet.cell(row_index, 1).value
            rc1_value = str(rc1_value)
            if rc1_value and "材料名称：（）" in rc1_value:
                unit = [f.unit_name for f in bfoods if f.name == name]
                unit = unit[0] if len(unit) > 0 else "斤"
                sheet.cell(row_index, 1, f"材料名称：{name}（{unit}）")

        return sheet

    def get_data_rows_list(self,sheet):
        rows = []
        for row in sheet.iter_rows(
            min_row=1, 
            max_row=sheet.max_row,  
            min_col=1,
            max_col=14
        ):
            cell3 = row[2]
            if "摘要" in str(cell3.value):
                rows.append([row.row+1,None])
                continue
            elif "本月合计" in str(cell3.value):
                row_m1 = rows[-1]
                row_m1[-1] = row.row-1
                rows[-1] = row_m1
                continue
            pass
        return rows

    def make_row_counts_same(self):
        ldata_rows = self.get_data_rows_list(lsheet) 
        cdata_rows = self.get_data_rows_list(csheet)

            for i,(crow0,crow1) in enumerate(cdata_rows):
                lrow0,lrow1 = ldata_rows[i]
                row_diff =  (lrow1-lrow0) - (crow1-crow0):
                if row_diff > 0:
                    csheet.insert_rows(crow0+1,row_diff)
                pass        
        pass


    def start(self):
        lwb = self.last_wb
        cwb = self.current_wb

        lwb_sheet_names = self.get_food_sheet_names(lwb)
        cwb_sheet_names = self.get_food_sheet_names(cwb)

        
        for name in lwb_sheet_names:
            if not name in cwb_sheet_names:
                sheet = lwb[name] 
                cwb.copy_worksheet(sheet)
                pass
            else
                lsheet = lwb[name]
                csheet = cwb[name]
                ldata_rows = self.get_data_rows_list(lsheet) 
                cdata_rows = self.get_data_rows_list(csheet)
                
                for i,(crow0,crow1) in enumerate(cdata_rows):
                    lrow0,lrow1 = ldata_rows[i]
                    row_diff =  (lrow1-lrow0) - (crow1-crow0):

                    if row_diff > 0:
                        csheet.insert_rows(crow0+1,row_diff)
                    
                    pass
                


                

        
    pass

# The end.
