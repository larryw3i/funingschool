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
        pass

    @property
    def p_spreadsheet_fpath(self):
        saved_wb_name_key = _("Saved Purchase or Daybook Spreadsheet Names")
        title = _("Select a spreadsheet")
        label = _("File:")
        tooltip = _("Select a Purchase SpreadSheet or Daybook Spreadsheet.")
        fpath = self.user.cfg.select(saved_wb_name_key, title, label, tooltip)
        self._p_spreadsheet_fpath = self.dpath / fpath
        return self._p_spreadsheet_fpath

    @property
    def foods(self):

        pass

    pass


# The end.
