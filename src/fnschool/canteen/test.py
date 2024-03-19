import os
import sys
from pathlib import Path
import unittest

sys.path.append(Path(__file__).parent.parent.parent.as_posix())

from fnschool import *
from fnschool.canteen import *
from fnschool.canteen.bill import *
from fnschool.canteen.profile import *


class TestCanteen(unittest.TestCase):
    def spreadsheet_by_time_nodes(self):
        bill = Bill()
        bill.set_profile_to_index0()
        bill.workbook.purchase_workbook_fd_path = (
            Path.home() / "Downloads"
        ).as_posix()
        for m in range(2, 4):
            bill.set_month(m)
            bill.print_month()
            bill.make_spreadsheet_by_time_nodes()
            bill.workbook.copy_workbook()

    def print_time_nodes(self):
        bill = Bill()
        bill.print_time_nodes()

    def get_foods(self):
        bill = Bill()
        bill.set_profile_to_index0()
        bill.workbook.purchase_workbook_fd_path = (
            Path.home() / "Downloads"
        ).as_posix()
        for m in range(2, 4):
            bill.set_month(m)
            time_nodes = bill.get_time_nodes_of_month()
            for time_node in time_nodes:
                bill.time_node = time_node
                bill._foods = None
                if bill.foods:
                    print(time_node)
                    print(*bill.foods)
                else:
                    print(time_node, "Nothing.")


if __name__ == "__main__":
    unittest.main()

# The end.
