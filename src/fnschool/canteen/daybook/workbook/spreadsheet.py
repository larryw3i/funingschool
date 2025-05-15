import os
import sys
from fnschool.canteen.daybook.workbook import *
from fnschool.canteen.daybook.workbook.purchase import *


class SpreadSheet(FileBase):
    def __init__(self, note):
        SpreadSheetBase.__init__(self, note)
        self.wb = Workbook()
        self._purchase = None

        pass

    @property
    def purchase(self):
        if not self._purchase:
            self._purchase = Purchase(self)
        return self._purchase
        pass


# The end.
