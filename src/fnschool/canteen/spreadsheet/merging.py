import os
import random
import sys
from pathlib import Path
import shutil
import secrets
import calendar
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

import tkinter as tk
from tkinter import filedialog, ttk

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *

from fnschool.canteen.spreadsheet.base import Base
from fnschool.canteen.spreadsheet.food import Food as FoodSheet


class Merging(Base):
    def __init__(self, bill):
        super().__init__(bill)
        self._last_fpath = None
        self._current_fpath = None
        self.last_fpath_dpath_key = _("last_bill_dpath")
        self.current_fpath_dpath_key = _("current_bill_dpath")
        self._last_wb = None
        self._current_wb = None
        self._food_sheet = None
        pass

    @property
    def food_sheet(self):
        if not self._food_sheet:
            self._food_sheet = FoodSheet(self.bill)
        return self._food_sheet

    @property
    def last_wb(self):
        if not self._last_wb:
            print_info(_('Loading data from "{0}".').format(self.last_fpath))
            wb = load_workbook(self.last_fpath, data_only=True)
            self._last_wb = wb
        return self._last_wb

    @property
    def current_wb(self):
        if not self._current_wb:
            print_info(_('Loading data from "{0}".').format(self.current_fpath))
            wb = load_workbook(self.current_fpath)
            self._current_wb = wb
        return self._current_wb

    @current_wb.setter
    def current_wb(self, wb):
        self._current_wb = wb
        pass

    @property
    def last_fpath(self):
        if not self._last_fpath:
            root = tk.Tk()
            root.withdraw()
            conf_initialdir = self.config.get(self.last_fpath_dpath_key)
            conf_initialdir = Path(conf_initialdir) if conf_initialdir else None
            initialdir = conf_initialdir or documents_dpath or Path.home()
            fpath = filedialog.askopenfilename(
                parent=root,
                title=_("Select the last bill spreadsheet"),
                initialdir=initialdir,
                filetypes=self.filetypes_xlsx,
            )
            if not fpath:
                print_error(_("there is not file selected. Exit."))
                exit()
            else:
                fpath = Path(fpath)

            if not conf_initialdir == fpath:
                self.config.save(self.last_fpath_dpath_key, fpath.parent)
            self._last_fpath = fpath

        return self._last_fpath
        pass

    @property
    def current_fpath(self):
        if not self._current_fpath:
            root = tk.Tk()
            root.withdraw()
            conf_initialdir = self.config.get(self.current_fpath_dpath_key)
            conf_initialdir = Path(conf_initialdir) if conf_initialdir else None
            initialdir = conf_initialdir or documents_dpath or Path.home()
            fpath = filedialog.askopenfilename(
                parent=root,
                title=_("Select the current bill spreadsheet"),
                initialdir=initialdir,
                filetypes=self.filetypes_xlsx,
            )

            if not fpath:
                print_error(_("there is not file selected. Exit."))
                exit()
            else:
                fpath = Path(fpath)

            if not conf_initialdir == fpath:
                self.config.save(self.current_fpath_dpath_key, fpath.parent)

            self._current_fpath = fpath
        return self._current_fpath
        pass

    def get_food_sheet_names(self, wb):
        names = []
        for name in wb.sheetnames:
            sheet = wb[name]
            if sheet.cell(1, 1).value and self.food_form_title_like in str(
                sheet.cell(1, 1).value
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

    def get_data_rows_list(self, sheet):
        rows = []
        for row in sheet.iter_rows(
            min_row=1, max_row=sheet.max_row, min_col=1, max_col=14
        ):
            cell3 = row[2]
            if "摘要" in str(cell3.value):
                rows.append([cell3.row + 1, None])
                continue
            elif "本月合计" in str(cell3.value):
                row_m1 = rows[-1]
                row_m1[-1] = cell3.row - 1
                rows[-1] = row_m1
                continue
            pass
        return rows

    def make_row_counts_same(self, last_sheet, current_sheet):
        lsheet = last_sheet
        csheet = current_sheet
        ldata_rows = self.get_data_rows_list(lsheet)
        cdata_rows = self.get_data_rows_list(csheet)

        for i, (crow0, crow1) in enumerate(cdata_rows):
            lrow0, lrow1 = ldata_rows[i]
            row_diff = (lrow1 - lrow0) - (crow1 - crow0)
            if row_diff > 0:
                csheet.insert_rows(crow0 + 1, row_diff)
                for row_index_f in range(crow0 + 1, crow0 + 1 + row_diff):
                    for col_index_f in range(1, 14):
                        cell = csheet.cell(row_index_f, col_index_f)
                        cell.border = self.cell_border0
                        cell.alignment = self.cell_alignment0
                self.make_row_counts_same(lsheet, csheet)
                break
            elif row_diff < 0:
                row_diff = abs(row_diff)
                lsheet.insert_rows(lrow0 + 1, row_diff)
                for row_index_f in range(lrow0 + 1, lrow0 + 1 + row_diff):
                    for col_index_f in range(1, 14):
                        cell = lsheet.cell(row_index_f, col_index_f)
                        cell.border = self.cell_border0
                        cell.alignment = self.cell_alignment0
                self.make_row_counts_same(lsheet, csheet)
                break

            pass

        pass

    def start(self, current_wb=[None, None]):
        lwb = self.last_wb

        if current_wb:
            current_wb, current_fpath = current_wb

            self.current_fpath = current_fpath
            self.current_wb = current_wb

        cwb = self.current_wb

        lwb_sheet_names = self.get_food_sheet_names(lwb)
        cwb_sheet_names = self.get_food_sheet_names(cwb)

        names_len = len(lwb_sheet_names)
        names_len2 = len(str(names_len))
        name_index = 0
        for name in lwb_sheet_names:
            lsheet = None
            csheet = None
            if not name in cwb_sheet_names:
                lsheet = lwb[name]
                csheet = cwb.create_sheet(lsheet.title, -1)
                for row in lsheet.iter_rows(max_col=13):
                    for lcell in row:
                        ccell = csheet.cell(lcell.row, lcell.column)
                        ccell.value = lcell.value
                        ccell.alignment = self.cell_alignment0
                        ccell.border = self.cell_border0
                    csheet.row_dimensions[row[0].row].height = self.row_height
                self.food_sheet.format(csheet)
                pass
            else:
                lsheet = lwb[name]
                csheet = cwb[name]

                self.unmerge_sheet_cells(csheet)

                self.make_row_counts_same(lsheet, csheet)
                ldata_rows = self.get_data_rows_list(lsheet)
                cdata_rows = self.get_data_rows_list(csheet)
                row_offset = 2

                for (lrow0, lrow1), (crow0, crow1) in list(
                    zip(ldata_rows, cdata_rows)
                ):
                    for row_i in range(lrow1 + row_offset - lrow0):
                        lrow = lrow0 + row_i
                        crow = crow0 + row_i

                        for col_i in range(1, 14):

                            cell_value = csheet.cell(crow, col_i).value

                            if not (
                                cell_value
                                or str(cell_value)
                                .replace(" ", "")
                                .replace("　", "")
                                == ""
                            ):
                                ccell = csheet.cell(
                                    crow,
                                    col_i,
                                )
                                ccell.value = lsheet.cell(lrow, col_i).value
                                pass

                        csheet.row_dimensions[crow0 + row_i].height = (
                            self.row_height
                        )

                        pass

                    pass

            name_index += 1
            print(
                Fore.RED
                + f"[{name_index:>{names_len2}}/{names_len}] "
                + Style.RESET_ALL
                + Fore.GREEN
                + _(
                    'Data from Sheet "{0}" of Workbook "{1}" was '
                    + 'copied to Sheet"{2}" of Workbook "{3}".'
                ).format(
                    lsheet.title,
                    self.last_fpath,
                    csheet.title,
                    self.current_fpath,
                )
                + Style.RESET_ALL
            )

            self.food_sheet.update_summation(csheet)
            self.food_sheet.update_inventories(csheet)

            csheet.sheet_properties.tabColor = secrets.token_hex(4)
            print_info(
                _('Food sheet "{0}" has its color recolor.').format(
                    csheet.title
                )
            )

            self.food_sheet.format(csheet)

            lsheet = None
            csheet = None

            pass

        print_info(
            _('Merge completed！Saving "{0}".').format(self.current_fpath)
        )
        cwb.save(self.current_fpath)

        lwb = None
        cwb = None

        open_path(self.current_fpath)

    pass


# The end.
