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

    def get_entry_index(self, form_index):

        sheet_title = self.sheet.title

        form_index0, form_index1 = form_index
        if sheet_title == self.s.unwarehousing_name:
            entry_index0, entry_index1 = form_index0 + 2, form_index1 - 1
        elif sheet_title == self.s.warehousing_name:
            entry_index0, entry_index1 = form_index0 + 2, form_index1 - 1
        elif sheet_title == self.s.consuming_name:
            entry_index0, entry_index1 = form_index0 + 2, form_index1 - 1
        elif sheet_title == self.s.inventory_name:
            entry_index0, entry_index1 = form_index0 + 3, form_index1 - 1

        return [entry_index0, entry_index1]

    def del_form_empty_row(self, col_index):
        col_index = col_index
        self.del_form_indexes()
        form_indexes = self.form_indexes

        for form_index in form_indexes:
            entry_index0, entry_index1 = self.get_entry_index(form_index)

            entry_len = (entry_index1 - entry_index0) + 1
            len_diff = entry_len - self.entry_row_len0
            if len_diff > 0:
                for row_index in range(entry_index0, entry_index1 + 1):
                    if not self.sheet.cell(row_index, col_index).value:
                        self.sheet.delete_rows(row_index, 1)
                        print_warning(
                            _(
                                'Empty row {0} of sheet "{1}" has been deleted.'
                            ).format(row_index, self.sheet.title)
                        )
                        entry_index1 = entry_index1 - 1
                        len_diff = len_diff - 1
                        if row_index == entry_index1 or len_diff < 1:
                            break


# The end.
