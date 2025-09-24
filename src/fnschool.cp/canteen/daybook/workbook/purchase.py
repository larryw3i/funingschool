import os
import sys

from fnschool.canteen.daybook.workbook import *


class Purchase(SheetBase):
    def __init__(self, spreadsheet):
        SheetBase.__init__(self, spreadsheet)
        self._foods = None
        self._counting_date_col_index = None
        self._meal_type_col_index = None
        self._name_col_index = None
        self._quantity_col_index = None
        self._total_price_col_index = None
        self._residual_col_index = None
        self._negligible_col_index = None

        self._p_spreadsheet = None
        self._p_spreadsheet_fpath = None
        self._p_sheet = None
        self._daybook_spreadsheet_selected = False
        pass

    @property
    def p_spreadsheet_fpath(self):
        saved_wb_name_key = _("Saved Purchase or Daybook Spreadsheet Names")
        title = _("Select a spreadsheet")
        label = _("File:")
        tooltip = _("Select a Purchase SpreadsheetFile or Daybook Spreadsheet.")
        fpath = self.user.cfg.select(saved_wb_name_key, title, label, tooltip)
        p_spreadsheet_fpath = self.file.dpath / fpath
        if not p_spreadsheet_fpath.exists():
            wb0 = Workbook()
            wb.save(p_spreadsheet_fpath)

        self._p_spreadsheet_fpath = p_spreadsheet_fpath
        return self._p_spreadsheet_fpath

    @property
    def daybook_spreadsheet_selected(self):
        spreadsheet = None
        if self._p_spreadsheet:
            spreadsheet = self._p_spreadsheet
        else:
            spreadsheet = load_workbook(
                self.p_spreadsheet_fpath, read_only=True
            )
        if self.purchase_original_sheet_name in spreadsheet.sheetnames:
            self._daybook_spreadsheet_selected = True
        else:
            self._daybook_spreadsheet_selected = False
        return self._daybook_spreadsheet_selected
        pass

    @property
    def p_spreadsheet(self):
        if not self._p_spreadsheet:
            p_spreadsheet = load_workbook(self._p_spreadsheet_fpath)
            self._p_spreadsheet = p_spreadsheet
        return self._p_spreadsheet
        pass

    @property
    def p_sheet(self):
        if not self._p_sheet:
            p_sheet = (
                self.p_spreadsheet[self.purchase_original_sheet_name]
                if self.daybook_spreadsheet_selected
                else self.p_spreadsheet[self.p_spreadsheet.sheetnames[0]]
            )
            self._p_sheet = p_sheet
        return self._p_sheet

    @property
    def foods(self):

        pass

    pass


# The end.
