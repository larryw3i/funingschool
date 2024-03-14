
import os
import sys
from pathlib import Path
import unittest

sys.path.append(
    Path(__file__).parent.parent.parent.as_posix()
)
from fnschool import *
from fnschool.canteen import *
from fnschool.canteen.bill import *
from fnschool.canteen.profile import *


class TestCateen(unittest.TestCase):
    def test_update_check_inventory_sheet_from_changsheng_like(self):
        bill = Bill()
        bill.set_profile(
            Profile().get_profile0()
        )
        cs_fpath = (
            Path(__file__).parent.parent.parent.parent / "tests" / "files" / "changsheng.3.1-3.15.xlsx" 
        ).as_posix()
        bill.workbook.update_check_inventory_sheet_from_changsheng_like(
            file_path = cs_fpath
        )
        bill.workbook.copy_workbook()

if __name__ == '__main__':
    unittest.main()
