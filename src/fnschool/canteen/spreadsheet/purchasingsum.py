import os
import sys

from fnschool import *
from fnschool.canteen.spreadsheet.base import SpreadsheetBase


class PurchasingSum(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = "入库、未入库汇总表"
        pass

    def update(self):
        time_nodes = [
            tn
            for tn in self.bill.get_time_nodes()
            if tn[1].month == self.bill.month
        ]
        t0, t1 = time_nodes[-1]
        pssheet = self.get_purchase_sum_sheet()

        pssheet.cell(
            2,
            1,
            f"编制单位：{self.bill.profile.org_name}"
            + f"        "
            + f"单位：元"
            + f"         "
            + f"{t1.year}年{t1.month}月{t1.day}日",
        )
        pssheet.cell(
            20,
            1,
            f"编制单位：{self.bill.profile.org_name}"
            + f"        "
            + f"单位：元"
            + f"         "
            + f"{t1.year}年{t1.month}月{t1.day}日",
        )
        foods = [
            f
            for f in self.food.get_foods()
            if (not f.is_residue and f.check_date.month == self.bill.month)
        ]
        wfoods = [f for f in foods if not f.is_negligible]
        uwfoods = [f for f in foods if f.is_negligible]
        total_price = 0.0
        for row in pssheet.iter_rows(
            min_row=4, max_row=10, min_col=1, max_col=3
        ):
            class_name = row[0].value.replace(" ", "")
            _total_price = 0.0
            for food in wfoods:
                if food.class_name == class_name:
                    _total_price += food.count * food.unit_price
            pssheet.cell(row[0].row, 2, _total_price)
            total_price += _total_price
        total_price_cn = self.bill.convert_num_to_cnmoney_chars(total_price)
        pssheet.cell(
            11, 1, f"总金额（大写)：{total_price_cn}    ¥{total_price:.2f}"
        )
        pssheet.cell(12, 1, f"经办人：{self.bill.profile.name}  ")

        total_price = sum([f.count * f.unit_price for f in uwfoods])
        total_price_cn = self.bill.convert_num_to_cnmoney_chars(total_price)
        pssheet.cell(27, 2, total_price)
        pssheet.cell(
            29, 1, f"总金额（大写)：{total_price_cn}    ¥{total_price:.2f}"
        )

        pssheet.cell(30, 1, f"经办人：{self.bill.profile.name}  ")

        wb = self.get_bill_workbook()
        wb.active = pssheet

        print_info(_("Sheet '%s' was updated.") % self.purchase_sum_sheet_name)


# The end.
