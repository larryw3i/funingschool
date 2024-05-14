import os
import sys
import calendar
from datetime import datetime, date, time, timedelta
import colorama

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.workbook import *
from fnschool.canteen.profile import *
from fnschool.canteen.path import *
from fnschool.canteen.config import *


class Bill:
    def __init__(self):
        self._food = None
        self._checked_foods = None
        self.bill_workbook = None
        self._config = None
        self._time_nodes = []
        self._time_node = None
        self._month = None
        self._quiet = False
        self._profile = None
        self._foods = []
        self.verbose = 0
        self.show_init_msg = True
        self.currency_unit0 = "元"
        pass

    @property
    def get_foods(self):
        return self.foods.get_foods()

    @property
    def config(self):
        if not self._config:
            self._config = Config()
        return self._config

    def strs_are_equal(self, str_value, like):
        not_like_list = None
        if "!" in like:
            like = like.split("!")
            not_like_list = like[1:]
            like = like[0]
        result = (
            str_value.endswith(like[1:])
            if (like.startswith("*") and not like.endswith("*"))
            else (
                str_value.startswith(like[:-1])
                if (like.endswith("*") and not like.startswith("*"))
                else (
                    str_value == like
                    if like.startswith("=")
                    else (
                        like[1:-1] in str_value
                        if (like.startswith("*") and like.endswith("*"))
                        else str_value == like
                    )
                )
            )
        )
        if not_like_list:
            result = result and not any(
                [self.strs_are_equal(str_value, nlk) for nlk in not_like_list]
            )

        return result

    @property
    def time_node(self):
        return self.get_time_node()

    @time_node.setter
    def time_node(self, node):
        self._time_node = node

    def get_time_node_index(self, time_node=None):
        time_node = time_node or self.time_node
        if time_node in self.time_nodes:
            return self.time_nodes.index(time_node)
        return None

    def get_check_times(self, time_node):
        tn_index = self.get_time_node_index(time_node)
        t0, t1 = time_node
        if tn_index > 0:
            return [self.time_nodes[tn_index - 1][1], t1 + timedelta(days=-1)]
        else:
            return [t0 + timedelta(days=-3), t1 + timedelta(days=-1)]

    def get_check_times_of_time_node(self):
        if not self.time_node:
            return None
        tn_index = self.get_time_node_index()
        t0, t1 = self.time_node
        if tn_index > 0:
            return [self.time_nodes[tn_index - 1][1], t1 + timedelta(days=-1)]
        else:
            return [t0 + timedelta(days=-3), t1 + timedelta(days=-1)]

    @property
    def month(self):
        return self.get_month()

    def set_month(self, month):
        self._month = month

    def get_month(self):
        if self._month:
            return self._month

        months_info = _(
            "Enter the month (1~12) to generate spreadsheet: (default: {0})"
        ).format(datetime.now().month)
        months = [str(i) for i in range(1, 13)] + [""]

        for __ in range(3):
            print_info(months_info)
            _month = input(">_ ")
            if not _month in months:
                continue
            else:
                if _month == "":
                    self._month = datetime.now().month
                else:
                    self._month = int(_month)
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
        if not self.bill_workbook:
            self.bill_workbook = WorkBook(self)
        return self.bill_workbook

    @property
    def time_nodes(self):
        return self.get_time_nodes()

    def get_year(self):
        print_info(_("Please input the year for design consuming"))

    def get_time_nodes(self):
        if len(self._time_nodes) < 1:
            d_now = datetime.now()
            _time_nodes = calendar.monthcalendar(d_now.year, self.get_month())

            if 0 in _time_nodes[0]:
                _time_nodes[0] = [d for d in _time_nodes[0] if d > 0]
            if 0 in _time_nodes[-1]:
                _time_nodes[-1] = [d for d in _time_nodes[-1] if d > 0]

            self._time_nodes = [
                [
                    datetime.combine(
                        datetime(d_now.year, self.get_month(), tn[0]),
                        time(0, 0, 0),
                    ),
                    datetime.combine(
                        datetime(d_now.year, self.get_month(), tn[-1]),
                        time(0, 0, 0),
                    ),
                ]
                for tn in _time_nodes
            ]

        return self._time_nodes

    def help_friends_via_email(self):
        print_warning("Hello!")
        pass

    def print_time_nodes(self):
        time_nodes_str = []
        _count = 1
        for t0, t1 in self.get_time_nodes():
            time_nodes_str.append(
                str(_count)
                + ". "
                + _("{0}.{1}.{2}--{3}.{4}.{5}").format(
                    t0.year, t0.month, t0.day, t1.year, t1.month, t1.day
                )
            )

            _count += 1
        del _count

        time_nodes_str = "\t".join(time_nodes_str)
        print_warning(_("Time nodes:"))
        print_info(time_nodes_str)

    def print_check_time_range(self):
        if not self.time_node:
            print(_("Time node hasn't been set."))
            return
        t0, t1 = self.time_node
        ckt0, ckt1 = self.get_check_times_of_time_node()
        print_info(
            _("Food checking time range of {0} is {1}.").format(
                t0.strftime("%Y.%m.%d") + "-->" + t1.strftime("%Y.%m.%d"),
                ckt0.strftime("%Y.%m.%d") + "-->" + ckt1.strftime("%Y.%m.%d"),
            )
        )

    def print_month(self):
        print_info(_("Month:") + str(self.get_month()))

    def print_basic_info(self):
        self.print_time_nodes()
        self.print_profile()
        self.print_month()

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

    @property
    def is_fncht(self):
        return "富宁城投" in self.profile.suppliers

    @property
    def is_xuelan(self):
        return "雪兰" in self.profile.suppliers

    @property
    def is_changsheng(self):
        return "昌盛" in self.profile.suppliers

    def show_msg(self):
        has_tip = False
        print_info(
            _("The configuration directory is: {0}").format(
                canteen_config_fpath.parent
            )
        )
        if any([self.is_changsheng, self.is_xuelan]):
            has_tip = True
            print_warning(_("Hello! helping information is here for you:"))
        if self.is_changsheng:
            print_info(
                _(
                    "Tips for Changsheng files:\n"
                    + "You need to add the residue of last year "
                    + "or last semester: Open the first "
                    + "spreadsheet you got from Changsheng, "
                    + "and add the 'residue' column, then "
                    + "insert the 'residue' foods after the end "
                    + "of entered data, the 'residue' column names "
                    + "you could set are:\n\t{0}\n"
                    + "The columns need to be updated are:"
                    + "\n\t1. Inventory time: The time of residue "
                    + "foods inventorying."
                    + "\n\t2. The organization name or school name."
                    + "\n\t3. The food name."
                    + "\n\t4. The food count, fill in all count related columns if "
                    + "there are many 'food count columns'."
                    + "\n\t5. The total price."
                ).format(" | ".join(self.workbook.residue_col_names))
            )

        if self.is_xuelan:
            print_info(
                _(
                    "If new Xuelan milks is purchased. you have to "
                    + "add the purchasing information of them into "
                    + "the end of the purchasing spreadsheet (e.g: "
                    + "the spreadsheets Changsheng provided)."
                )
            )
        if has_tip:
            print_warning(_("Ok! I knew that.(press any key to continue)"))
            input(">_ ")

    def make_spreadsheet_by_time_nodes(self):
        self.set_profile_to_index0()
        self.print_basic_info()

        self.get_time_nodes()
        self.get_month()
        self.food.get_foods()
        time_nodes = self.get_time_nodes_of_month()

        if self.show_init_msg:
            self.show_msg()

        for time_node in time_nodes:
            self.time_node = time_node
            self.print_check_time_range()
            self.make_spreadsheet_by_time_node()

    def make_spreadsheets(self):
        self.set_profile_to_index0()
        self.show_msg()
        self.print_basic_info()
        self.get_time_nodes()
        self.get_month()

        self.workbook.update_sheets()
        pass

    def set_profile_to_index0(self):
        self.set_profile(Profile().get_profiles()[0])

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
        tn = self.get_time_node()
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

    def get_time_node(self):
        return self._time_node

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
            "仟",
            "万",
            "拾",
            "佰",
            "仟",
            "亿",
            "拾",
            "佰",
            "仟",
            "万",
            "拾",
            "佰",
            "仟",
            "兆",
        ]

        format_num = [
            "零",
            "壹",
            "贰",
            "叁",
            "肆",
            "伍",
            "陆",
            "柒",
            "捌",
            "玖",
        ]
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
