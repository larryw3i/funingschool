import os
import sys

from fnschool import *
from fnschool.canteen import *
from fnschool.canteen.bill import *
from fnschool.canteen.config import *


class FoodBase:
    def __init__(self, bill):
        self.bill = bill
        self.workbookbase = self.bill.workbookbase


class Food:
    def __init__(
        self,
        bill,
        name=None,
        fid=None,
        unit_price=0.0,
        total_price=0.0,
        check_date=None,
        count=0.0,
        consuming_list=None,
        is_residue=False,
        is_blank=False,
        is_negligible=False,
        unit_name=None,
    ):
        self.bill = bill
        self.config = self.bill.config
        self.name = name
        self.fid = fid
        self._unit_price = unit_price
        self._total_price = total_price
        self._count = count
        self.is_residue = is_residue
        self.check_date = check_date
        self.consuming_list = consuming_list or []
        self.get_food_list_method0 = None
        self.food_list_fpath0 = None
        self._main_spreadsheet_path = None
        self._check_df = None
        self.is_negligible = is_negligible
        self.consume = self.add_consumption
        self.residue_mark = "(R)"
        self.is_blank = is_blank
        self.unit_name = unit_name or "市斤"
        self.unit_names = None
        self.recounts = None
        self._foods = []
        pass

    @property
    def unit_price(self):
        if self._unit_price:
            return self._unit_price
        if self._total_price and self._count:
            return self._total_price / self._count

    @property
    def count(self):
        if self._count:
            return self._count
        if self._total_price and self._unit_price:
            return self._total_price / self._unit_price

    @property
    def total_price(self):
        if self._total_price:
            return self._total_price
        if self._unit_price and self._count:
            return self._unit_price * self._count

    @property
    def workbook(self):
        return self.bill.workbook

    def get_name_with_residue_mark(self):
        return (
            (self.name + self.residue_mark)
            if (
                self.is_residue
                or (self.remainder > 0 and len(self.consuming_list) > 0)
            )
            else self.name
        )

    def __str__(self, newline=True):
        return (
            " ".join(
                [
                    self.name,
                    self.class_name,
                    str(self.unit_price)
                    + self.bill.currency_unit0
                    + "/"
                    + self.unit_name
                    + "*"
                    + str(self.count)
                    + self.unit_name
                    + "="
                    + str(self.total_price)
                    + self.bill.currency_unit0,
                    _("Is residue") if self.is_residue else "",
                    _("Is neglibible") if self.is_negligible else "",
                ]
            )
            + (
                (
                    "\n\t"
                    + _("Consuming records:")
                    + "\n\t"
                    + "\n\t".join(
                        [
                            d.strftime("%Y%m%d") + "->" + str(c)
                            for d, c in self.consuming_list
                        ]
                    )
                )
                if len(self.consuming_list) > 0
                else ""
            )
            + ("\n" if newline else "")
        )

    def get_residue_foods(self, month):
        foods = self.get_non_negligible_foods()
        time_nodes = [
            tn for tn in self.bill.get_time_nodes() if tn[0].month == month
        ]
        time_nodes_mm1 = [
            tn for tn in self.bill.get_time_nodes() if tn[0].month == month - 1
        ]
        if len(time_nodes_mm1) > 0:
            time_nodes = [time_nodes_mm1[-1]] + time_nodes

        _foods = []
        for tn in time_nodes:
            _foods.append(
                [
                    tn,
                    [
                        f
                        for f in foods
                        if (
                            f.check_date < tn[1]
                            and f.get_remainder_by_time(tn[1]) > 0
                        )
                    ],
                ]
            )

        return _foods

    def get_remainder_by_time(self, time):
        return self.count - sum(
            [c for d, c in self.consuming_list if d <= time]
        )

    @property
    def workbook(self):
        return self.bill.workbook

    def get_non_negligible_foods(self):
        foods = self.get_foods()
        foods = [f for f in foods if not f.is_negligible]
        return foods

    def get_negligible_foods_of_time_node(self):
        foods = self.get_foods_of_time_node()
        foods = [f for f in foods if f.is_negligible]
        return foods

    def get_residue_foods_of_time_node(self):
        if not self._foods:
            return []
        foods = self.get_non_negligible_foods_of_time_node()
        foods = [f for f in foods if f.is_residue_of_time_node()]
        return foods

    def get_count(self):
        return self.count

    def add_consumption(self, time_point, count):
        self.consuming_list.append([time_point, count])

    @property
    def remainder(self):
        return self.get_remainder()

    def get_remainder(self):
        return self.get_count() - sum(
            [count for time_point, count in self.consuming_list]
        )

    def clean_count(self, name, count, unit):
        recounts = self.config.get_food_recounts()
        for _name, _unit, _times in recounts:
            if _unit == unit and self.bill.strs_are_equal(name, _name):
                return count * _times
        return count

    def clean_unit_name(self, name=None):
        if not self.unit_names:
            self.unit_names = self.config.get_food_unit_names()

        name = name or self.name
        for _name_like, _unit in self.unit_names:
            if self.bill.strs_are_equal(name, _name_like):
                return _unit
        return "市斤"

    def get_class_names(self):
        class_names_cfg = self.bill.config.get_food_classes()
        class_names = list(class_names_cfg.keys())
        class_names = ["蔬菜类"] + class_names
        return class_names

    @property
    def class_name(self, name=None):
        name = name or self.name
        classes = self.config.get_food_classes()
        for _class, name_likes in classes.items():
            if any(
                [self.bill.strs_are_equal(name, like) for like in name_likes]
            ):
                return _class
        return "蔬菜类"

    def set_get_food_list_method0(self, method_n=None):
        self.get_food_list_method0 = str(method_n)

    def set_food_list_fpath0(self, file_path=None):
        self.food_list_fpath0 = file_path

    def get_checked_foods(self):
        food_list = self.get_food_list_from_check_sheet()
        return food_list

    def convert_text_lines_to_foods(self, text_lines):
        foods = [
            self.convert_text_line_to_food(text_line)
            for text_line in text_lines
        ]

        if None in foods:
            foods.remove(None)

        return foods

    def convert_text_line_to_food(self, text_line):
        values = re.split("\s+", text_line)
        content_error_str = _(f"line '%s' has been discarded.") % (text_line)
        values_len = 6
        if "" in values:
            values.remove("")
        if len(values) != values_len:
            print_error(
                content_error_str,
                "\n",
                _("values length is less than %s.") % (values_len),
            )
            return None
        (
            food_uuid,
            food_check_date,
            food_name,
            food_count,
            food_total_price,
            food_is_residue,
        ) = values

        if not (
            str.isnumeric(food_count.replace(".", ""))
            and str.isnumeric(food_total_price.replace(".", ""))
        ):
            print_error(
                content_error_str,
                "\n",
                _("Food count: %s") % (food_count),
                "\n",
                _("Food total price: %s") % (food_total_price),
            )
            return None

        if not (str.isnumeric(food_check_date) and len(food_check_date) == 8):
            print_error(
                content_error_str,
                "\n",
                _("Food check date: %s") % (food_check_date),
            )
            return None

        food_check_date = datetime(
            int(food_check_date[:4]),
            int(food_check_date[4:6]),
            int(food_check_date[6:]),
        )
        food_count = float(food_count)
        food_total_price = float(food_total_price)
        food_is_residue = food_is_residue.strip() in "是Yy"

        return Food(
            fid=food_uuid,
            canteen=self.bill,
            name=food_name,
            check_date=food_check_date,
            count=food_count,
            unit_price=food_total_price / food_count,
            total_price=food_total_price,
            is_residue=food_is_residue,
        )

    @property
    def is_new(self):
        return not self.is_residue

    def get_new_foods_total_price(self):
        foods = self.bill.get_food_list()
        return sum([food.total_price for food in foods if not food.is_residue])

    def get_residue_total_price(self):
        foods = self.bill.get_food_list()
        return sum([food.total_price for food in foods if food.is_residue])

    def is_residue_of_time_node(self):
        foods = self.get_non_negligible_foods_of_time_node()
        foods = [
            f
            for f in foos
            if (f.count - sum([c for d, c in f.consuming_list])) > 0
        ]
        return foods

    def get_purchased_count_of_residue(self, fid):
        check_df = self.workbook.get_check_df()
        if check_df is None:
            return 0
        for index, row in check_df.iterrows():
            is_residue = row["是留存"] == ""
            if index == fid and not is_residue.strip() in "是Yy":
                return float(row["数量"])
        print(f"Couldn't find the food by '{fid}'.")
        return None

    def get_checked_foods_by_time_node_m1(self):
        return self.query_foods_by_time_node(
            self.get_food_list_from_check_sheet(),
            self.bill.get_time_nodes()[-1],
        )

    def get_foods_of_month(self, month):
        foods = []
        time_nodes = self.bill.get_time_nodes()
        time_nodes = [t for t in time_nodes if t[0].month == month]
        time_node_cp = self.bill.time_node
        for time_node in time_nodes:
            self.bill.time_node = time_node
            _foods = self.get_foods_of_time_node()
            for _f in _foods:
                if not _f in foods:
                    foods.append(_f)
        self.bill.time_node = time_node_cp
        return foods

    def get_purchased_foods(self):
        self.workbook.read_changsheng_foods()

        return self.bill._foods

    def get_foods(self):
        if not self.bill._foods:
            self.get_purchased_foods()
            print_info(
                _("The directory of consuming files is: {0}").format(
                    self.workbook.get_profile_copy_data_dpath()
                )
            )
            self.set_consumption_of_foods()
        return self.bill._foods

    def set_consumption_of_foods(self):
        self.workbook.read_consumptions_from_pre_consuming_workbooks()
        print_info(_("Consumptions were read."))

    def get_foods_of_time_node(self):
        foods = self.get_foods()
        t0, t1 = self.bill.get_time_node()
        ckt0, ckt1 = self.bill.get_check_times_of_time_node()

        foods = [f for f in foods if (ckt0 <= f.check_date <= ckt1)]
        return foods

    @property
    def time_node_foods(self):
        return self.get_foods_of_time_node()

    @property
    def time_node_residue_foods(self):
        foods = self.time_node_foods
        if not foods:
            return None
        foods = [f for f in foods if f.is_residue]
        return foods

    def get_foods_from_pre_consuming_sheet_by_time_node(self):
        time_start, time_end = self.bill.get_time_node()
        time_nodes = [
            t
            for t in self.bill.get_time_nodes()
            if self.bill.times_are_same_year_month(t[0], time_end)
        ]
        foods = []
        for time_node in time_nodes:
            foods += self.get_foods_from_pre_consuming_sheet(
                self.workbook.get_pre_consuming_sheet_name_by_time_node(
                    time_node
                )
            )

        foods = sorted(foods, key=lambda f: f.check_date)
        return foods

    def get_foods_from_pre_consuming_sheet_m1(self):
        foods = self.get_foods_from_pre_consuming_sheet(
            self.workbook.get_pre_consuming_sheet_name_by_time_node(
                self.bill.get_time_nodes()[-1]
            )
        )
        return foods

    def get_foods_from_pre_consuming_sheet(self, name):
        pcsheet = self.workbook.get_bill_sheet(name)
        row_index_offset = self.workbook.pre_consuming_sheet_row_index_offset
        col_index_offset = self.workbook.pre_consuming_sheet_col_index_offset
        foods = self.get_food_list()
        new_foods = []
        for row in pcsheet.iter_rows(
            min_row=row_index_offset, max_row=pcsheet.max_row
        ):
            fid = row[0].value
            if not fid:
                break
            food = self.get_food_from_list_by_id(foods, fid)
            if not food:
                continue
            for col_index in range(col_index_offset, pcsheet.max_column + 1):
                count = row[col_index - 1].value
                if count:
                    if not pcsheet.cell(1, col_index).value:
                        continue
                    time_point = pcsheet.cell(1, col_index).value.split(".")
                    time_point = datetime(
                        int(time_point[0]),
                        int(time_point[1]),
                        int(time_point[2]),
                    )
                    food.consum(time_point, float(count))

            if not food in new_foods:
                new_foods.append(food)

        return new_foods


# The end.
