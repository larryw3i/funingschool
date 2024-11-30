import os
import sys
from fnschool.canteen.food import *
from fnschool.canteen.spreadsheet.base import *


class ConsumingSum(Base):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = self.s.consumingsum_name
        pass

    def update(self):
        cssheet = self.sheet
        year = self.bill.consuming.year
        month = self.bill.consuming.month
        day = self.consuming_day_m1
        foods = [f for f in self.bfoods if not f.is_abandoned]

        total_price = 0.0
        for row in cssheet.iter_rows(
            min_row=4, max_row=10, min_col=1, max_col=3
        ):
            class_name = row[0].value.replace(" ", "")
            m_total_price = 0.0
            for food in foods:
                if food.fclass == class_name:
                    m_total_price += sum(
                        [
                            _count * food.unit_price
                            for _date, _count in food.consumptions
                        ]
                    )

            m_total_price = round(m_total_price, self.sd + 1)
            total_price += m_total_price
            cssheet.cell(row[0].row, 2, m_total_price)
            cssheet.cell(row[0].row, 2).number_format = numbers.FORMAT_NUMBER_00

        total_price = round(total_price, self.sd + 1)
        local_total_price = self.get_local_total_price(total_price)
        cssheet.cell(
            1,
            1,
            (
                self.bill.operator.superior_department
                + _("食堂食品、材料出库汇总报销单")
            ),
        )
        cssheet.cell(
            2,
            1,
            _("编制单位：")
            + f"{self.purchaser}       "
            + _("单位：元")
            + f"         "
            + _("{0}年{1}月{2}日").format(year, month, day),
        )
        cssheet.cell(
            11,
            1,
            (
                _("总金额（大写）")
                + f"：{local_total_price}    "
                + f"{self.currency.mark}{total_price}"
            ),
        )
        cssheet.cell(12, 1, _("经办人：") + f"{self.operator.name}  ")

        wb = self.bwb
        wb.active = cssheet

        print_info(_("Sheet '%s' was updated.") % self.sheet.title)


# The end.
