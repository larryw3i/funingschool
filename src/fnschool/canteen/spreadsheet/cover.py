import os
import sys
from fnschool import *
from fnschool.canteen.spreadsheet.base import *


class Cover(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = self.s.cover_name
        pass

    def update(self):
        year = self.bill.consuming.year
        month = self.bill.consuming.month
        day = self.consuming_day_m1

        cvsheet = self.sheet
        cvsheet.cell(
            1,
            1,
            self.purchaser + f"{year}年{month}月份食堂食品采购统计表",
        )
        foods = [f for f in self.bfoods if (not f.is_inventory)]
        wfoods = [f for f in foods if not f.is_abandoned]
        uwfoods = [f for f in foods if f.is_abandoned]
        total_price = 0.0
        for row in cvsheet.iter_rows(
            min_row=3, max_row=9, min_col=1, max_col=3
        ):
            class_name = row[0].value.replace(" ", "")
            m_total_price = 0.0
            for f in foods:
                if f.fclass == class_name:
                    m_total_price += f.count * f.unit_price
            cvsheet.cell(row[0].row, 2, m_total_price)

            total_price += m_total_price
        cvsheet.cell(10, 2, total_price)

        w_seasoning_total_price = sum(
            [f.count * f.unit_price for f in wfoods if ("调味" in f.fclass)]
        )
        unw_seasoning_total_price = sum(
            [f.count * f.unit_price for f in uwfoods if ("调味" in f.fclass)]
        )

        for row_index in range(3, 11):
            cvsheet.cell(row_index, 3, "")

        cvsheet.cell(
            8,
            3,
            f"入库：{w_seasoning_total_price:.2f}元；"
            + f"未入库：{unw_seasoning_total_price:.2f}元",
        )

        wb = self.bwb
        wb.active = cvsheet

        print_info(_("Sheet '%s' was updated.") % self.sheet.title)


# The end.
