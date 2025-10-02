import os
import sys
import tkinter as tk
import tomllib
from tkinter import filedialog, ttk

from openpyxl.utils.cell import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *
from fnschool.canteen.spreadsheet.base import *


class Purchasing(SsBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.name = self.s.purchasing_name
        self.p_dpath_key = _("Parent Path Of Purchasing File")

    @property
    def foods(self):
        pass

    @property
    def wb(self):
        if not self._wb:
            print_info(_('Loading data from "{0}".').format(self.path))
            self._wb = load_workbook(self.path)
        return self._wb

    @property
    def food_classes(self):
        food_classes = self.bill.food_classes
        return food_classes

    @property
    def path(self):
        p_dpath = self.cfg.get(self.p_path_key)
        initialdir = (
            p_dpath
            if (p_dpath and Path(p_dpath).exists())
            else ((Path.home() / "Downloads").as_posix())
        )
        if not self._path:
            self.gui.show_info(
                _(
                    "{0} need a purchasing list file, "
                    + "and it's file type should be '.xlsx'. "
                    + "The column names of it:"
                ).format(app_name)
                + _(
                    ""
                    + "\n\t ______________________________________________"
                    + "\n\t| column       | type  | example   | Note      |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Checking Date| Text  | 2024-03-01|           |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Food Name    | Text  | Cabbage   |           |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Meal Type    | Text  | Breakfast | Optional  |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Count        | Number| 20        |           |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Unit         | Text  | jin1      |           |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Total Price  | Number| 20.0      |           |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Is Negligible| Text  | y         |           |"
                    + "\n\t|``````````````|```````|```````````|```````````|"
                    + "\n\t| Is Inventory | Text  | y         |           |"
                    + "\n\t ``````````````````````````````````````````````"
                )
            )

            filetypes = ((_("Spreadsheet Files"), "*.xlsx"),)

            tkroot = tk.Tk()
            tkroot.withdraw()
            tkroot.attributes("-topmost", True)

            filename = filedialog.askopenfilename(
                parent=tkroot,
                title=_("Please select the purchasing file"),
                initialdir=initialdir,
                filetypes=filetypes,
            )

            if filename is None or filename == ():
                print_warning(_("No file was selected, exit."))
                exit()
                return None
            print_info(
                _('Purchasing list file "{0}" has been selected.').format(
                    filename
                )
            )
            self._path = filename
        self.cfg.set(self.p_dpath_key, Path(self._path).parent.as_posix())
        return self._path

    def update_data_validations(self):
        if not self.food_class_dv in self.sheet.data_validations:
            self.sheet.add_data_validation(self.food_class_dv)

    def update(self):
        pass


# The end.
