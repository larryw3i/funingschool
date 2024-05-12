import os
import sys
from fnschool import *
from fnschool.canteen.spreadsheet.base import SpreadsheetBase


class Cover(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = "六大类总封面"
        pass

    def update(self):
        time_nodes = self.bill.get_time_nodes()
        t0, t1 = time_nodes[-1]
        cvsheet = self.get_conver_sheet()
        cvsheet.cell(
            1,
            1,
            self.bill.profile.org_name
            + f"{t1.year}年{t1.month}月份食堂食品采购统计表",
        )
        foods = [
            f
            for f in self.food.get_foods()
            if (not f.is_residue and f.check_date.month == self.bill.month)
        ]
        wfoods = [f for f in foods if not f.is_negligible]
        uwfoods = [f for f in foods if f.is_negligible]
        total_price = 0.0
        for row in cvsheet.iter_rows(
            min_row=3, max_row=9, min_col=1, max_col=3
        ):
            class_name = row[0].value.replace(" ", "")
            _total_price = 0.0
            for f in foods:
                if f.fclass == class_name:
                    _total_price += f.count * f.unit_price
            cvsheet.cell(row[0].row, 2, _total_price)

            total_price += _total_price
        cvsheet.cell(10, 2, total_price)

        w_seasoning_total_price = sum(
            [f.count * f.unit_price for f in wfoods if ("调味" in f.fclass)]
        )
        unw_seasoning_total_price = sum(
            [
                f.count * f.unit_price
                for f in uwfoods
                if ("调味" in f.fclass)
            ]
        )

        cvsheet.cell(
            8,
            3,
            f"入库：{w_seasoning_total_price:.2f}元；"
            + f"未入库：{unw_seasoning_total_price:.2f}元",
        )

        if self.bill.is_changsheng and self.bill.is_xuelan:
            self.update_cover_sheet_for_cangsheng_xuelan(
                cvsheet, foods, wfoods, uwfoods, total_price
            )

        wb = self.get_bill_workbook()
        wb.active = cvsheet

        print_info(_("Sheet '%s' was updated.") % self.cover_sheet_name)
