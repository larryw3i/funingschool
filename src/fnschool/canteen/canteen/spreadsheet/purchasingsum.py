import os
import sys

from fnschool import *
from fnschool.canteen.spreadsheet.base import *


class PurchasingSum(Base):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = self.s.purchasingsum_name
        pass

    def update(self):

        pssheet = self.sheet
        year = self.bill.consuming.year
        month = self.bill.consuming.month
        day = self.consuming_day_m1

        pssheet.cell(
            1,
            1,
            (
                self.bill.operator.superior_department
                + "食堂食品、材料入库汇总报销单"
            ),
        )
        pssheet.cell(
            19,
            1,
            (
                self.bill.operator.superior_department
                + "食堂食品、材料未入库汇总报销单"
            ),
        )
        pssheet.cell(
            2,
            1,
            f"编制单位：{self.purchaser}"
            + f"        "
            + f"单位：元"
            + f"         "
            + f"{year}年{month}月{day}日",
        )
        pssheet.cell(
            20,
            1,
            f"编制单位：{self.purchaser}"
            + f"        "
            + f"单位：元"
            + f"         "
            + f"{year}年{month}月{day}日",
        )
        foods = [f for f in self.bfoods if (not f.is_inventory)]

        wfoods = [f for f in foods if not f.is_abandoned]
        uwfoods = [f for f in foods if f.is_abandoned]
        total_price = 0.0

        for row in pssheet.iter_rows(
            min_row=4, max_row=10, min_col=1, max_col=3
        ):
            class_name = row[0].value.replace(" ", "")
            _total_price = 0.0
            for food in wfoods:
                if food.fclass == class_name:
                    _total_price += food.count * food.unit_price
            pssheet.cell(row[0].row, 2, _total_price)
            total_price += _total_price

        total_price_CNY = self.bill.get_CNY_chars(total_price)
        pssheet.cell(
            11, 1, f"总金额（大写)：{total_price_CNY}    ¥{total_price:.2f}"
        )
        pssheet.cell(12, 1, f"经办人：{self.operator.name}  ")

        total_price = sum([f.count * f.unit_price for f in uwfoods])
        total_price_CNY = self.bill.get_CNY_chars(total_price)
        pssheet.cell(27, 2, total_price)
        pssheet.cell(
            29, 1, f"总金额（大写)：{total_price_CNY}    ¥{total_price:.2f}"
        )

        pssheet.cell(30, 1, f"经办人：{self.operator.name}  ")

        wb = self.bwb
        wb.active = pssheet

        print_info(_("Sheet '%s' was updated.") % self.sheet.title)


# The end.
