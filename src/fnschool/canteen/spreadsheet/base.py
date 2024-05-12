import os
import sys
from openpyxl.styles import *
from openpyxl.formatting.rule import *
from openpyxl.styles.differential import *
from openpyxl.utils.cell import *


from fnschool import *


class SpreadsheetBase:
    def __init__(self, bill):
        self.bill = bill
        self.spreadsheet = self.bill.spreadsheet
        self.s = self.spreadsheet
        self.bill_workbook = self.spreadsheet.bill_workbook
        self.bwb = self.bill_workbook
        self.sheet_name = None
        self._sheet = None
        self._form_indexes = None
        self.cell_alignment0 = Alignment(horizontal="center", vertical="center")
        self.cell_side0 = Side(border_style="thin")
        self.cell_border0 = Border(
            top=self.cell_side0,
            left=self.cell_side0,
            right=self.cell_side0,
            bottom=self.cell_side0,
        )

    def row_inserting_tip(self, row_index):
        print_error(
            _(
                "Row {0} of {1} is being inserted, " + "please wait a moment."
            ).format(row_index, self.sheet.title)
        )

    def del_form_indexes(self):
        self._form_indexes = None

    @property
    def consuming_day_m1(self):
        dates = []
        for f in self.bfoods:
            dates += [d for d, __ in f.consumptions]
        date = max(dates)
        return date.day
        

    @property
    def bill_foods(self):
        return self.bill.foods

    @property
    def bfoods(self):
        return self.bill_foods

    @property
    def purchaser(self):
        return self.bill.purchaser

    @property
    def operator(self):
        return self.bill.operator

    def get_bill_sheet(self, name):
        sheet = self.bwb[name]
        return sheet

    def unmerge_sheet_cells(self, sheet=None):
        sheet = sheet or self.sheet
        if isinstance(sheet, str):
            sheet = self.get_bill_sheet(sheet)
        merged_ranges = list(sheet.merged_cells.ranges)
        for cell_group in merged_ranges:
            sheet.unmerge_cells(str(cell_group))
        print_info(_("Cells of {0} was unmerged.").format(sheet.title))

    @property
    def sheet(self):
        if not self.sheet_name:
            return None
        if not self._sheet:
            self._sheet = self.get_bill_sheet(self.sheet_name)
        return self._sheet


# The end.
