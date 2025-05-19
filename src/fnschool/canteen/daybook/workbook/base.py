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
        SpreadSheetBase.__init__(self, self.spreadsheet.note)
        self._wb = None
        pass

    @property
    def wb(self):
        if not self._wb:
            self._wb = self.spreadsheet.wb
        return self._wb

    pass


# The end.
