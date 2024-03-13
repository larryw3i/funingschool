import os
import sys
import colorama
from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.workbook import *
from fnschool.canteen.friend import *


class Bill:
    def __init__(self):
        self.food = Food(self)
        self._food_list = None
        self.workbook = WorkBook(self)
        self.time_nodes = []
        self._quiet = False
        self._friend = None
        self.org_name = None
        pass

    def help_friends_via_email(self):
        print_warning("Hello!")
        pass

    def make_spreadsheet_of_month(self):
        # self.set_profile("ly")
        # self.set_time_nodes(
        #     [
        #         (datetime(2024, 2, 26), datetime(2024, 2, 29)),
        #         # (datetime(2024,3,1), datetime(2024,3,1)),
        #     ]
        # )

        # canteen.workbook.get_warehousing_sheet().insert_rows(4,20)
        # canteen.workbook.copy_workbook()

        # canteen.food.get_foods_from_pre_consuming_sheet_by_time_nodes_m1(
        #     canteen.get_time_nodes()[0][1]
        # )

        # print(*canteen.workbook.get_residual_foods_by_month_m1())

        # canteen.workbook.update_check_inventory_sheet_from_cen_hang_xlsx()
        # canteen.workbook.update_consuming_sheet_by_time_node_m1()
        # canteen.workbook.update_inventory_sheet_by_time_node_m1()
        # canteen.workbook.update_check_sheet_by_time_node_m1()
        # canteen.workbook.update_warehousing_sheet_by_time_node_m1()
        # canteen.workbook.update_unwarehousing_sheet_by_time_node_m1()
        # canteen.workbook.update_consuming_sum_sheet()
        # canteen.workbook.update_purchase_sum_sheet_by_time_nodes_m1()
        # canteen.workbook.update_cover_sheet()
        # canteen.workbook.update_food_sheets_by_time_nodes_m1()
        print_info("Hello!")
        pass

    def set_friend(self, label):
        self._friend = Friend().get_friend_by_label(label)

    @property
    def friend(self):
        if self._friend:
            return self._friend
        print(_("Please configure friends."))
        return None

    def times_are_same_year_month(self, *times):
        time0 = times[0]
        for time in times[1:]:
            if time0.strftime("%Y%m") != time.strftime("%Y%m"):
                return False
        return True

    def set_profile(self, name):
        friend = None
        if isinstance(name, str) and name in self.friends.keys():
            friend = self.friends[name]
        else:
            friend= name
        self.set_org_name(profile[0])
        self.set_friend(profile[1])
        self.set_suppliers(profile[2])
        self.workbook.set_main_spreadsheet_path(profile[3])

    def set_suppliers(self, names):
        self.suppliers = names

    def set_friend(self, name):
        self.friend = name

    def set_org_name(self, name):
        self.org_name = name

    def set_quiet(self, value=False):
        self._quiet = value

    def get_time_nodes_m1(self):
        return self.get_time_nodes()[-1]

    @property
    def quiet(self):
        return self.get_quiet()

    def get_quiet(self):
        return self._quiet

    def get_food_list(self):
        if not self._food_list:
            self._food_list = self.food.get_food_list()
        return self._food_list

    def set_time_nodes(self, time_nodes):
        self.time_nodes = time_nodes

    def get_time_nodes(self):
        return self.time_nodes

    def clear_time_nodes(self):
        self.time_nodes = None

    def convert_num_to_cnmoney_chars(self, number=None):
        format_word = [
            "分",
            "角",
            "元",
            "拾",
            "佰",
            "千",
            "万",
            "拾",
            "佰",
            "千",
            "亿",
            "拾",
            "佰",
            "千",
            "万",
            "拾",
            "佰",
            "千",
            "兆",
        ]

        format_num = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
        if type(number) == str:
            if "." in number:
                try:
                    number = float(number)
                except:
                    print(_("%s can't change.") % number)
            else:
                try:
                    number = int(number)
                except:
                    print(_("%s   can't change.") % number)

        if type(number) == float:
            real_numbers = []
            for i in range(len(format_word) - 3, -3, -1):
                if number >= 10**i or i < 1:
                    real_numbers.append(int(round(number / (10**i), 2) % 10))

        elif isinstance(number, int):
            real_numbers = []
            for i in range(len(format_word), -3, -1):
                if number >= 10**i or i < 1:
                    real_numbers.append(int(round(number / (10**i), 2) % 10))

        else:
            print(_("%s can't change") % number)

        zflag = 0
        start = len(real_numbers) - 3
        cnmoney_strs = []
        for i in range(start, -3, -1):
            if 0 < real_numbers[start - i] or len(cnmoney_strs) == 0:
                if zflag:
                    cnmoney_strs.append(format_num[0])
                    zflag = 0
                cnmoney_strs.append(format_num[real_numbers[start - i]])
                cnmoney_strs.append(format_word[i + 2])

            elif 0 == i or (0 == i % 4 and zflag < 3):
                cnmoney_strs.append(format_word[i + 2])
                zflag = 0
            else:
                zflag += 1

        if cnmoney_strs[-1] not in (format_word[0], format_word[1]):
            cnmoney_strs.append("整")

        return "".join(cnmoney_strs)

# The end.
