import os
import sys
from fnschool.canteen.food import *
from fnschool.canteen.spreadsheet.base import SpreadsheetBase


class ConsumingSum(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        pass

    def update(self):
        cssheet = self.get_consuming_sum_sheet()
        time_nodes = sorted(
            [
                tn
                for tn in self.bill.get_time_nodes()
                if tn[1].month == self.bill.month
            ]
        )
        t0, t1 = time_nodes[-1]
        foods = [
            f
            for f in self.food.get_foods()
            if (self.bill.month in [d.month for d, c in f.consuming_list])
        ]

        total_price = 0.0
        for row in cssheet.iter_rows(
            min_row=4, max_row=10, min_col=1, max_col=3
        ):
            class_name = row[0].value.replace(" ", "")
            _total_price = 0.0
            for food in foods:
                if food.class_name == class_name:
                    _total_price += sum(
                        [
                            _count * food.unit_price
                            for _date, _count in food.consuming_list
                            if _date.month == self.bill.month
                        ]
                    )
            total_price += _total_price
            cssheet.cell(row[0].row, 2, _total_price)
            cssheet.cell(row[0].row, 2).number_format = numbers.FORMAT_NUMBER_00

        total_price_cn = self.bill.convert_num_to_cnmoney_chars(total_price)
        cssheet.cell(
            2,
            1,
            f"编制单位：{self.bill.profile.org_name}       "
            + f"单位：元         "
            + f"{t1.year}年{t1.month}月{t1.day}日",
        )
        cssheet.cell(
            11,
            1,
            (f"总金额（大写)：{total_price_cn}    " + f"¥{total_price:.2f}"),
        )
        cssheet.cell(12, 1, f"经办人：{self.bill.profile.name}  ")

        wb = self.get_bill_workbook()
        wb.active = cssheet

        print_info(_("Sheet '%s' was updated.") % self.consuming_sum_sheet_name)


# The end.
