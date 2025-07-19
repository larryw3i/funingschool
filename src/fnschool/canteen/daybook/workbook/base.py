import os
import sys
from fnschool.canteen.daybook.workbook import *


class FileBase(ABC):
    def __init__(self, note):
        self.note = note
        self.app = self.note.app
        self.user = self.note.user
        self.cfg = self.note.cfg

        pass


class SheetBase(FileBase):
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet
        self.file = self.spreadsheet
        FileBase.__init__(self, self.spreadsheet.note)
        self._wb = None
        self._sheet = None

        self.counting_date_col_names = [
            _("Counting Date"),
            _("Purchase Date"),
            _("Check Date"),
            _("Counting Date 0"),
            _("Counting Date 1"),
            _("Counting Date 2"),
            _("Counting Date 3"),
        ]
        self.meal_type_col_names = [
            _("Meal Type"),
            _("Meal Class"),
            _("Meal Type 0"),
            _("Meal Type 1"),
            _("Meal Type 2"),
            _("Meal Type 3"),
        ]
        self.name_col_names = [
            _("Name"),
            _("Food Name"),
            _("Food Name 0"),
            _("Food Name 1"),
            _("Food Name 2"),
            _("Food Name 3"),
        ]
        self.quantity_col_names = [
            _("Quantity"),
            _("Quantity 0"),
            _("Quantity 1"),
            _("Quantity 2"),
            _("Quantity 3"),
        ]
        self.total_price_col_names = [
            _("Total Price"),
            _("Total Price 0"),
            _("Total Price 1"),
            _("Total Price 2"),
            _("Total Price 3"),
        ]
        self.residual_col_names = [
            _("Residual"),
            _("Surplus"),
            _("Remnant"),
            _("Residual 0"),
            _("Residual 1"),
        ]
        self.negligible_col_names = [
            _("Negligible"),
            _("Neglected"),
            _("Non-inbound"),
            _("Negligible 0"),
            _("Negligible 1"),
        ]

        self.cover_sheet_name = _("Cover sheet")
        self.purchase_sum_sheet_name = _("Purchase sum sheet")
        self.purchase_list_sheet_name = _("Purchase list sheet")
        self.purchase_original_sheet_name = _("Original purchase sheet")
        self.consumption_sum_sheet_name = _("Consumption sum sheet")
        self.consumption_list_sheet_name = _("Consumption list sheet")
        self.surplus_sheet_name = _("Surplus sheet")

        pass

    @property
    def wb(self):
        if not self._wb:
            self._wb = self.spreadsheet.wb
        return self._wb

    @property
    def sheet(self):
        if not self._sheet(self):
            sheet = None
            wb_sheet_names = self.wb.sheetnames
            if self.name in wb_sheet_names:
                sheet = self.wb[self.name]
            else:
                sheet = self.wb.create_sheet(self.name)
            self._sheet = sheet
        return self._sheet
        pass

    pass


# The end.
