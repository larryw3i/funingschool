import os
import sys
from openpyxl.styles import *
from openpyxl.formatting.rule import *
from openpyxl.styles.differential import *
from openpyxl.utils.cell import *


from fnschool import *
from fnschool.canteen.spreadsheet.base import *


class Workbook:
    def __init__(self, bill, path=None):
        self.path = path or self.bill.operator.bill_fpath

    pass
