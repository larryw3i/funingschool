
import os
import sys
from fnschool import _

try:
    from .sett1ngs import operators
except:
    print(
        _("Please refer to file  to customize your 'sett1ngs.py' file.")
    )

class Operator():
    def __init__(
        self,
        label = None,
        name = None,
        email = None,
        school = None,
        suppliers = None
    ):
        self.label = label
        self.name = name
        self.email = email
        self.school = school
        self.suppliers = suppliers


    def get_operator_by_key(self,key):
        operator = operators.get(key,None)
        if not operator:
            return None

        return Operator(
            label = key,
            name = operator[0],
            email = operator[1],
            school = operator[2],
            suppliers = operator[3]
        )

    def get_operators(self):
        operators = []
        for key in operator.keys():
            value = operator.get(key)
            operators.append(
                Operator(
                    label = key,
                    name = operator[0],
                    email = operator[1],
                    school = operator[2],
                    suppliers = operator[3]
                )
            )
        return operators

class Bill():
    def __init__(self):
        self.food = Food(self)
        self._food_list = None
        self.workbook = WorkBook(self)
        self.time_nodes = []
        self._quiet = False
        self._operator = None
        self.org_name = None
        pass

    def set_operator(self,key):
        self._operator = Operator().get_operator_by_key(key)
       
    @property
    def operator(self):
        if self._operator:
            return self._operator
        print("Please set operator.")
        return None

    def times_are_same_year_month(self, *times):
        time0 = times[0]
        for time in times[1:]:
            if time0.strftime("%Y%m") != time.strftime("%Y%m"):
                return False
        return True

    def set_profile(self, name):
        if isinstance(name, str) and name in self.roll.keys():
            profile = self.roll[name]
        else:
            profile = name
        self.set_org_name(profile[0])
        self.set_operator(profile[1])
        self.set_suppliers(profile[2])
        self.workbook.set_main_spreadsheet_path(profile[3])

    def set_suppliers(self, names):
        self.suppliers = names

    def set_operator(self, name):
        self.operator = name

    def print_info(self, *argv, **kwargs):
        print(Fore.GREEN, end="")
        print(*argv, **kwargs)
        print(Style.RESET_ALL, end="")

    def print_error(self, *argv, **kwargs):
        print(Fore.RED, end="")
        print(*argv, **kwargs)
        print(Style.RESET_ALL, end="")

    def print_warning(self, *argv, **kwargs):
        print(Fore.YELLOW, end="")
        print(*argv, **kwargs)
        print(Style.RESET_ALL, end="")

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
                    print("%s can't change." % number)
            else:
                try:
                    number = int(number)
                except:
                    print("%s   can't change." % number)

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
            print("%s can't change" % number)

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
        
