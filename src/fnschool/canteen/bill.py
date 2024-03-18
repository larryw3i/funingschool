import os
import sys
from datetime import datetime, date, time

import colorama

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.workbook import *
from fnschool.canteen.profile import *
from fnschool.canteen.path import *


class Bill:
    def __init__(self):
        self._food = None
        self._checked_foods = None
        self._workbook = None
        self._time_nodes = []
        self._time_node = None
        self._month = None
        self._quiet = False
        self._profile = None
        pass

    @property
    def month(self):
        return self.get_month()

    def get_month(self):
        global _
        if self._month:
            return self._month

        months = sorted(
            list(set([t0.month for t0, t1 in self.get_time_nodes()]))
        )
        months = [str(m) for m in months]

        months_info = (
            _("Setted months:")
            + " ".join(months)
            + "\n"
            + _("Enter the month above to generate spreadsheet:")
        )

        for _ in range(3):
            print_info(months_info)
            _month = input(">_")
            if not _month in months:
                continue
            else:
                self._month = _month
                return self._month

        print_error(_("Unexpected input was got."))
        sys.exit()

    @property
    def food(self):
        if not self._food:
            self._food = Food(self)
        return self._food

    @property
    def workbook(self):
        if not self._workbook:
            self._workbook = WorkBook(self)
        return self._workbook

    @property
    def time_nodes(self):
        return self.get_time_nodes()

    def get_time_nodes(self):
        if len(self._time_nodes) < 1:
            with open(canteen_config_fpath, "rb") as f:
                _time_nodes = tomllib.load(f).get("canteen").get("time_nodes")
                self._time_nodes = [
                    [
                        datetime.combine(t0, time(0, 0, 0)),
                        datetime.combine(t1, time(0, 0, 0)),
                    ]
                    for t0, t1 in _time_nodes
                ]

        return self._time_nodes

    def help_friends_via_email(self):
        print_warning("Hello!")
        pass

    def print_time_nodes(self):
        time_nodes_str = []
        _count = 1
        for t0, t1 in self.time_nodes:
            time_nodes_str.append(
                str(_count)
                + "> "
                + (
                    _("{0}.{1}.{2}--{3}.{4}.{5}").format(
                        t0.year, t0.month, t0.day, t1.year, t1.month, t1.day
                    )
                )
            )
            _count += 1
        del _count

        time_nodes_str = "\t".join(time_nodes_str)

        print_warning(_("Time nodes:"))

        print_info(time_nodes_str)

    def print_month(self):
        print_info(_("Month:") + self.get_month())

    def print_basic_info(self):
        self.print_time_nodes()
        self.print_profile()
        sel.print_month()

    def print_profile(self):
        print_warning(_("Profile:"))
        print_info(
            "\n\t".join(
                [
                    "\t" + _("Label:") + self.profile.label,
                    _("Name:") + self.profile.name,
                    _("Email:") + self.profile.email,
                    _("Organization Name:") + self.profile.org_name,
                    _("Suppliers:") + "|".join(self.profile.suppliers),
                ]
            )
        )

    def make_spreadsheet_by_time_node(self):
        profile0 = Profile().get_profiles()[0]
        self.set_profile(profile0)
        self.get_month()

        self.print_basic_info()

        if "昌盛" in self.profile.suppliers:
            self.workbook.update_check_inventory_sheet_from_changsheng_like()
        else:
            print_error(_("Please update the codes for your supplier."))
            return

        # self.workbook.update_consuming_sheet_by_time_node_m1()
        # self.workbook.update_inventory_sheet_by_time_node_m1()
        # self.workbook.update_check_sheet_by_time_node_m1()
        # self.workbook.update_warehousing_sheet_by_time_node_m1()
        # self.workbook.update_unwarehousing_sheet_by_time_node_m1()
        # self.workbook.update_consuming_sum_sheet()
        # self.workbook.update_purchase_sum_sheet_by_time_nodes_m1()
        # self.workbook.update_cover_sheet()
        # self.workbook.update_food_sheets_by_time_nodes_m1()
        # print_info(_("Update completely!"))
        pass

    @property
    def profile(self):
        if self._profile:
            return self._profile
        return None

    def set_profile(self, profile):
        if isinstance(profile, str):
            profiles = Profile().get_profiles()
            for p in profiles:
                if p.label == label:
                    self._profile = p
                    break
        else:
            self._profile = profile

    def get_year_month_of_time_node_m1(self):
        tn = self.get_time_nodes_m1()
        ym = tn.strftime("%Y%m")
        return ym

    def times_are_same_year_month(self, *times):
        time0 = times[0]
        for time in times[1:]:
            if time0.strftime("%Y%m") != time.strftime("%Y%m"):
                return False
        return True

    def set_quiet(self, value=False):
        self._quiet = value

    def get_time_nodes_m1(self):
        return self.get_time_nodes()[-1]

    @property
    def quiet(self):
        return self.get_quiet()

    def get_quiet(self):
        return self._quiet

    def get_checked_foods(self):
        if not self._checked_foods:
            self._checked_foods = self.food.get_checked_foods()
        return self._checked_foods

    def set_time_nodes(self, time_nodes):
        self._time_nodes = time_nodes

    def clear_time_nodes(self):
        self._time_nodes = None

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
                    print_info(_("%s can't change.") % number)
            else:
                try:
                    number = int(number)
                except:
                    print_info(_("%s can't change.") % number)

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
            print_info(_("%s can't change.") % number)

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
