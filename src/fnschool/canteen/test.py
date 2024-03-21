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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bill = Bill()
        self.bill.verbose = 3
        self.bill.set_profile_to_index0()
        self.bill.workbook.purchase_workbook_fd_path = (
            Path.home() / "Downloads"
        ).as_posix()

    def spreadsheet_by_time_nodes(self):
        self.bill.set_profile_to_index0()
        self.bill.workbook.purchase_workbook_fd_path = (
            Path.home() / "Downloads"
        ).as_posix()
        for m in range(2, 4):
            self.bill.set_month(m)
            self.bill.print_month()
            self.bill.make_spreadsheet_by_time_nodes()
            self.bill.workbook.copy_workbook()

    def print_time_nodes(self):
        self.bill.print_time_nodes()

    def get_foods(self):
        for m in range(2, 4):
            print("Foods of Month ", m, ":")
            print(list(self.bill.food.get_foods_of_month(m)))

        print("All foods:")
        print(list(self.bill.food.get_foods_of_time_nodes()))

    def get_foods_by_time_node(self):
        for m in range(2, 4):
            self.bill.set_month(m)
            time_nodes = self.bill.get_time_nodes_of_month()
            for time_node in time_nodes:
                self.bill.time_node = time_node
                self.bill._foods = None
                foods = self.bill.food.get_foods_of_time_node()
                if foods:
                    print(time_node)
                    print(foods)
                else:
                    print(time_node, "Nothing.")

    def get_changsheng_info_by_dir(self):
        for i in self.bill.workbook.get_changsheng_info_by_dir():
            print(i)

    def update_inventory_sheet_of_time_node(self):
        for m in range(2, 4):
            self.bill.set_month(m)
            time_nodes = self.bill.get_time_nodes_of_month()
            for time_node in time_nodes:
                print(time_node)
                self.bill.time_node = time_node
                self.bill._foods = None
                self.bill.workbook.update_
                self.bill.workbook.update_inventory_sheet_of_time_node()
                print("Updated.")


if __name__ == "__main__":
    unittest.main()

# The end.
