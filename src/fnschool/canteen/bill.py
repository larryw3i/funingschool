import os
import sys
from fnschool import *

from fnschool.canteen.spreadsheet import *


class Bill:
    def __init__(self):
        self._spreadsheet = None
        pass

    @property
    def spreadsheet(self):
        if not self._spreadsheet:
            self._spreadsheet = SpreadSheet(self)
        return self._spreadsheet

    def make_spreadsheets(self):
        self.spreadsheet.read_foods()
        pass


# The end.
