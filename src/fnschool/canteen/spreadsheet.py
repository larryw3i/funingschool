import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np


from fnschool import *
from fnschool.canteen.food import *

from tkinter import filedialog


class SpreadSheet:
    def __init__(self, bill):
        self.bill = bill
        self._path = None
        self.food_name_cols = ["商品名称", "食材名称", "食品名称"]
        self.food_name_col_name = None
        self.unit_name_cols = ["订货单位", "食材单位", "订购单位", "计量单位"]
        self.unit_name_col_name = None
        self.total_price_cols = ["总价", "折前金额", "折后金额", "总金额"]
        self.total_price_col_name = None
        self.xdate_cols = ["送货日期", "检查日期", "清点日期", "x日期", "日期"]
        self.xdate_col_name = None
        self.purchaser_name_cols = [
            "客户名称",
            "购买者",
            "购买者名称",
            "顾客名称",
            "下单单位名",
            "购入单位名",
        ]
        self.purchaser_name_col_name = None
        self.count_cols = ["总数", "数量", "下单数量", "订货数量", "发货数量"]
        self.count_col_name = None
        self.abandoned_cols = [
            "不计",
            "未入库",
            "非入库",
            "不需入库",
            "是非入库",
        ]
        self.abandoned_col_name = None
        self.inventory_cols = [
            "盘存",
            "存余",
            "结余",
            "剩余",
            "是剩余",
            "是盘存",
            "是结余",
        ]
        self.inventory_col_name = None

    @property
    def path(self):
        if not self._path:
            filetypes = ((_("Spreadsheet Files"), "*.xlsx"),)

            filename = filedialog.askopenfilename(
                title=_("Select a file"),
                initialdir=(Path.home() / "Downloads").as_posix(),
                filetypes=filetypes,
            )
            if filename is None:
                print_warning(_("No file was selected."))
                return None

            self._path = filename
        return self._path

    def set_col_names(self, columns):
        columns = list(columns)
        for column_name in columns:
            if column_name in self.food_name_cols:
                self.food_name_col_name = column_name
            if column_name in self.unit_name_cols:
                self.unit_name_col_name = column_name
            if column_name in self.count_cols:
                self.count_col_name = column_name
            if column_name in self.total_price_cols:
                self.total_price_col_name = column_name
            if column_name in self.abandoned_cols:
                self.abandoned_col_name = column_name
            if column_name in self.inventory_cols:
                self.inventory_col_name = column_name
            if column_name in self.purchaser_name_cols:
                self.purchaser_name_col_name = column_name
            if column_name in self.xdate_cols:
                self.xdate_col_name = column_name

        for col_name, col_names in [
            (self.food_name_col_name, self.food_name_cols),
            (self.unit_name_col_name, self.unit_name_cols),
            (self.count_col_name, self.count_cols),
            (self.total_price_col_name, self.total_price_cols),
            # (self.inventory_col_name,self.inventory_cols),
            # (self.abandoned_col_name,self.abandoned_cols),
            (self.xdate_col_name, self.xdate_cols),
            (self.purchaser_name_col_name, self.purchaser_name_cols),
        ]:
            if not col_name:
                print_error(
                    _("There should be column ({0}), please add it.").format(
                        "|".join(col_names)
                    )
                )
                exit()

    def read_foods(self):
        foods = pd.read_excel(self.path)
        self.set_col_names(foods.columns)
        _foods = []
        for __, food in foods.iterrows():
            _food = Food(
                self.bill,
                name=food[self.food_name_col_name],
                unit_name=food[self.unit_name_col_name],
                count=food[self.count_col_name],
                total_price=food[self.total_price_col_name],
                xdate=food[self.xdate_col_name],
                purchaser=food[self.purchaser_name_col_name],
            )
            if self.abandoned_col_name:
                _food.is_abandoned = not food[self.abandoned_col_name] is np.nan
            if self.inventory_col_name:
                _food.is_inventory = not food[self.inventory_col_name] is np.nan
            _foods.append(_food)

        foods = _foods
        foods = sorted(foods, key=lambda f: f.xdate)
        self.consuming(foods)
        return foods
        pass

    def consuming(self, foods):
        year = foods[-1].xdate.year
        month = foods[-1].xdate.month
        time_nodes = sorted(
            list(
                set(
                    [f.xdate for f in foods]
                    + [
                        datetime(
                            year,
                            month,
                            calendar.monthrange(year, month)[1],
                        )
                    ]
                )
            )
        )

        wb_fpath = self.get_pre_consuming_workbook_fpath()
        wb = load_workbook(wb_fpath)
        sheet = wb[self.pre_consuming_sheet0_name]

        foods = new_foods
        foods = [f for f in foods if not f.is_negligible]
        row_index_offset = self.pre_consuming_sheet_row_index_offset
        col_index_offset = self.pre_consuming_sheet_col_index_offset
        rc_index = 0
        days_difference = (t1 - t0).days

        for day in range(0, days_difference + 1):
            time_header = (t0 + timedelta(days=day)).strftime("%Y.%m.%d")
            cell = sheet.cell(1, rc_index + col_index_offset)
            cell.value = time_header
            cell.number_format = numbers.FORMAT_TEXT
            rc_index += 1

        rc_index = 0
        for row in sheet.iter_rows(
            max_col=5,
            min_row=row_index_offset,
            max_row=row_index_offset + len(foods),
        ):
            if rc_index > len(foods) - 1:
                break
            food = foods[rc_index]
            row[0].value = food.get_name_with_residue_mark()
            row[1].value = food.count
            row[3].value = food.unit_price
            rc_index += 1

        wb.active = sheet
        wb.save(wb_fpath)
        wb.close()
        print_warning(
            _(
                "Sheet '{0}' was updated.\n"
                + "Press any key to continue when you have "
                + "completed the foods allocation."
            ).format(sheet.title)
        )
        print_info(
            _("Ok! I have updated spreadsheet '{0}'. (Press any key)").format(
                wb_fpath
            )
        )
        open_file(wb_fpath)
        input()

        pass

    def update_sheets(self):
        pass


# The end.
