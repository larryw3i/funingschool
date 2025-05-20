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
        SpreadSheetBase.__init__(self, self.spreadsheet.note)
        self._wb = None
        self._sheet = None
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
