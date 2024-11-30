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
                + _("食堂食品、材料入库汇总报销单")
            ),
        )
        pssheet.cell(
            19,
            1,
            (
                self.bill.operator.superior_department
                + _("食堂食品、材料未入库汇总报销单")
            ),
        )
        pssheet.cell(
            2,
            1,
            _("编制单位：")
            + f"{self.purchaser}"
            + f"        "
            + _("单位：")
            + f"{self.currency.unit}"
            + f"         "
            + _("{0}年{1}月{2}日").format(year, month, day),
        )
        pssheet.cell(
            20,
            1,
            _("编制单位：")
            + f"{self.purchaser}"
            + f"        "
            + _("单位：")
            + self.currency.unit
            + f"         "
            + _("{0}年{1}月{2}日").format(year, month, day),
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
                    _total_price = round(_total_price, self.sd + 1)

            pssheet.cell(row[0].row, 2, _total_price)
            total_price += _total_price

        total_price = round(total_price, self.sd + 1)
        local_total_price = self.get_local_total_price(total_price)
        pssheet.cell(
            11,
            1,
            (
                _("总金额（大写）：")
                + f"{local_total_price}    "
                + f"{self.currency.mark}{total_price}"
            ),
        )
        pssheet.cell(12, 1, _("经办人：") + f"{self.operator.name}  ")

        total_price = sum([f.count * f.unit_price for f in uwfoods])
        local_total_price = self.bill.get_CNY_chars(total_price)
        pssheet.cell(27, 2, total_price)
        pssheet.cell(
            29,
            1,
            _("总金额（大写）：")
            + f"{local_total_price}    "
            + f"{self.currency.mark}{total_price}",
        )

        pssheet.cell(30, 1, _("经办人：") + f"{self.operator.name}  ")

        wb = self.bwb
        wb.active = pssheet

        print_info(_("Sheet '%s' was updated.") % self.sheet.title)


# The end.
