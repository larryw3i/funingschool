import os
import sys


class SpreadsheetBase:
    def __init__(self, bill):
        self.bill = bill
        self.spreadsheet = self.bill.spreadsheet
        self.s = self.spreadsheet
        self.bill_workbook = self.spreadsheet.bill_workbook
        self.bwb = self.bill_workbook 
        self.sheet_name = None
        self._sheet = None
        self.operator = self.bill.operator
    
    @property
    def bill_foods(self):
        return self.bill.foods

    @property
    def bfoods(self):
        return self.bill_foods

    
    def get_bill_sheet(self,name):
        sheet = self.bwb[name]
        return sheet 
    

    def unmerge_sheet_cells(self):
        sheet = self.sheet
        if isinstance(sheet, str):
            sheet = self.get_bill_sheet(sheet)
        merged_ranges = list(sheet.merged_cells.ranges)
        for cell_group in merged_ranges:
            sheet.unmerge_cells(str(cell_group))
        print_info(
            _("Cells of {0} was unmerged.").format(sheet.title)
        )

    @property
    def sheet(self):
        if not self.sheet_name:
            return None
        if not self._sheet:
            self._sheet = self.get_bill_sheet(self.sheet_name)
        return self._sheet

 

# The end.
