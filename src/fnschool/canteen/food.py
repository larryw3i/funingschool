import os
import sys

from fnschool import *
from fnschool.canteen import *
from fnschool.canteen.bill import *


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
    ):
        self.bill = bill
        self.name = name
        self.fid = fid
        self._unit_price = unit_price
        self._total_price = total_price
        self.check_date = check_date
        self._count = count
        self.is_residue = is_residue
        self.consuming_list = consuming_list or []
        self.get_food_list_method0 = None
        self.food_list_fpath0 = None
        self._main_spreadsheet_path = None
        self._base_class_df = None
        self._check_df = None
        self._unit_name = None
        self.consum = self.add_consumption
        self.residue_mark = "(R)"
        self.is_blank = is_blank
        pass

    @property
    def unit_price(self):
        if self._unit_price:
            return self._unit_price
        if self._total_price and self._count:
            return self._total_price/self._count
    
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

    def get_name_withresidue_mark(self):
        return (
            (self.name + self.residue_mark) if self.is_residue else self.name
        )

    def __str__(self, newline=True):
        return "\n" + "\n\t".join(
            [
                f"Name: {self.name}",
                f"UnitPrice: {self.unit_price}",
                f"Count: {self.count} ({self.unit_name})",
                f"TotalPrice: {self.total_price}",
                f"IsResidue: {self.is_residue}",
                f"CheckDate: {self.check_date}",
            ]
        )

    @property
    def workbook(self):
        return self.bill.workbook

    def get_count(self):
        return self.count

    def add_consumption(self, time_point, count):
        self.consuming_list.append([time_point, count])

    def get_remainder(self):
        return self.get_count() - sum(
            [count for time_point, count in self.consuming_list]
        )

    @property
    def unit_name(self):
        return self.get_unit_name()

    def get_unit_name(self, name=None):
        unit_df = self.workbook.get_unit_df()
        name = name or self.name
        unit = unit_df[unit_df["Name"] == name]["Unit"].tolist()
        return (
            unit[0]
            if unit
            else f'=VLOOKUP("{name}",{self.workbook.unit_sheet_name}!A:B,2,0)'
        )

    def name_in_unit_sheet(self):
        return self.name in self.workbook.get_unit_name_list()

    def get_base_class_name(self):
        base_class_df = self.workbook.get_base_class_df()
        for index, row in base_class_df.iterrows():
            if self.name in row.to_list():
                return index

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

    @property
    def is_negligible(self):
        class_list = self.workbook.get_negligible_class_list()
        return self.name in class_list

    def get_new_foods_total_price(self):
        foods = self.bill.get_food_list()
        return sum([food.total_price for food in foods if not food.is_residue])

    def get_residue_total_price(self):
        foods = self.bill.get_food_list()
        return sum([food.total_price for food in foods if food.is_residue])

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

    def check_name_in_unit_sheet(self, foods):
        food_names = []
        for food in foods:
            if not food.name_in_unit_sheet():
                food_names.append(food.name)
        if len(food_names) > 0:
            self.bill.print_warning(
                "Adding '" + " ".join(food_names) + "' to unit sheet."
            )
            self.workbook.add_food_names_to_unit_sheet(food_names)

    def get_food_list_from_check_sheet(self):
        check_df = self.workbook.get_check_df()
        if check_df is None:
            return None
        food_list = []
        row_index = 2
        food_id_list = []
        for index, row in check_df.iterrows():
            food_id = row["ID"]
            is_residue = str(row["是盘存"]) in "是Yy"
            if pd.isnull(food_id):
                food_id = str(uuid.uuid4())
                food_id_list.append((row_index, food_id))

            text_line = (
                f'{food_id} {row["时间"]} {row["材料名"]}'
                + f' {row["数量"]}'
                + f' {row["总价"]} '
                + ("Y" if is_residue else "N")
            )
            food_list.append(self.convert_text_line_to_food(text_line))
            row_index += 1

        if len(food_id_list) > 0:
            check_sheet = self.workbook.get_check_sheet()
            for row_index, food_id in food_id_list:
                check_sheet.cell(row_index, 1, food_id)

        if len(food_list) > 0:
            self.check_name_in_unit_sheet(food_list)
            self.check_name_in_base_class_sheet(food_list)
            return food_list

        return None

    def check_name_in_base_class_sheet(self, food_list):
        food_names = []
        for food in food_list:
            if not food.get_base_class_name():
                food_names.append(food.name)
        if len(food_names) > 0:
            self.bill.print_error(
                "Unclassified "
                + ("Foods" if len(food_list) > 1 else "Food")
                + ":\n"
                + ("\n".join(food_names))
            )

    def get_negligible_foods_by_time_node_m1(self):
        foods = self.get_checked_foods_by_time_node_m1()
        return [food for food in foods if food.is_negligible]

    def get_non_negligible_foods_by_time_node_m1(self):
        foods = self.get_checked_foods_by_time_node_m1()
        return [food for food in foods if not food.is_negligible]

    def get_checked_foods_by_time_node_m1(self):
        return self.query_foods_by_time_node(
            self.get_food_list_from_check_sheet(),
            self.bill.get_time_nodes()[-1],
        )

    def query_foods_by_time_node(self, foods, time_node):
        time_start, time_end = time_node
        time_nodes = self.bill.get_time_nodes()
        time_node_index = time_nodes.index(time_node)

        if time_node_index < 1:
            time_start = time_start - timedelta(days=1)
            time_end = time_end - timedelta(days=1)
        else:
            time_start = time_nodes[time_node_index - 1][0]
            time_start = time_nodes[time_node_index - 1][1]

        foods = [
            food for food in foods if time_start <= food.check_date <= time_end
        ]
        return foods

    def get_food_from_list_by_id(self, foods, fid):
        for food in foods:
            if food.fid == fid:
                return food
        return None

    def get_foods_from_pre_consuming_sheet_by_time_nodes_m1(self):
        time_start, time_end = self.bill.get_time_nodes_m1()
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
        pcsheet = self.workbook.get_sheet(name)
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
