import os
import sys

from fnschool.canteen.daybook.workbook import *


class Purchase(SheetBase):
    def ___init__(self, spreadsheet):
        SheetBase.__inir__(self, spreadsheet)
        self.name = _("Purchase")
        self._sheet = None

    pass


# The end.
