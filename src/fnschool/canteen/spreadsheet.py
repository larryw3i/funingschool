import os
import sys
from pathlib import Path
import shutil
import calendar
import pandas as pd
from datetime import datetime, timedelta
import numpy as np


from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *

from tkinter import filedialog


class SpreadSheet:
    def __init__(self, bill):
        self.bill = bill
        self._path = None
        self.pre_consuming_sheet_name = "出库计划表"
        self.pre_consuming_sheet_row_index_offset = 3
        self.pre_consuming_sheet_col_index_offset = 5
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
        self.consume_foods(foods)
        return foods
        pass

    def consume_foods(self, foods):
        cfoods = [f for f in foods if not f.is_abandoned]
        year = cfoods[-1].xdate.year
        month = cfoods[-1].xdate.month
        time_nodes = sorted(
            list(
                set(
                    [f.xdate for f in cfoods]
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
        print(time_nodes)

        wb_fpathes = []
        for i in range(1,len(time_nodes)):
            tn0, tn1 = time_nodes[i-1], time_nodes[i]
            if tn0.month != tn1.month:
                tn0 = datetime(tn1.year,tn1.month,1)
            wb_fpath = (self.bill.operator_consuming_dpath / (
                f"consuming-"
                + tn0.strftime("%Y.%m.%d")+"-"
                + tn1.strftime("%Y.%m.%d")+".xlsx"
            )).as_posix()

            wb_fpathes.append(wb_fpath)

        print(wb_fpathes)

        foods_list = []
        for xdate in list(set([f.xdate for f in cfoods])):
            foods_list.append([f for f in cfoods if f.xdate == xdate])

        for i,wb_fpath in enumerate(wb_fpathes):
            shutil.copy(pre_consuming0_fpath,wb_fpath)
            print_info(
                _("Spreadsheet \"{0}\" was copied to \"{1}\".").format(
                    pre_consuming0_fpath,wb_fpath
                )
            )
            wb = load_workbook(wb_fpath)
            sheet = wb[self.pre_consuming_sheet_name]
            tn1 = time_nodes[i+1]
            tn0 = time_nodes[i]
            if not tn0.month == tn1.month:
                tn0 = datetime(tn1.year, tn1.month,1)

            wbfoods = foods_list[i]
            wbfoods0 = [f for f in cfoods if f.get_remmainer(tn0) > 0]
            for wbfood in wbfoods0:
                wbfood.name = wbfood.name + _("(Residual)")
            wbfoods += wbfoods0

            for d_index in range(
                0,
                (tn1 - tn0).days + 1
            ):
                d_date = tn0+timedelta(days = d_index)
                sheet.cell(
                    1,
                    self.pre_consuming_sheet_col_index_offset+d_index,
                    d_date.strftime("%Y.%m.%d")
                )

            for f_index in range(
                0,
                len(wbfoods)
            ):
                wbfood = wbfoods[f_index]
                row_index = self.pre_consuming_sheet_row_index_offset+f_index
                sheet.cell(row_index,1, wbfood.name)
                sheet.cell(row_index,2, wbfood.get_remmainer(tn0))
                sheet.cell(row_index,4, wbfood.unit_price)
                
            wb.save(wb_fpath)
            print_warning(
                _(
                    "Sheet '{0}' was updated.\n"
                    + "Press any key to continue when you have "
                    + "completed the foods allocation."
                ).format(sheet.title)
            )
            wb.close()
            open_file(wb_fpath)
            print_info(
                _("Ok! I have updated spreadsheet '{0}'. (Press any key)").format(
                    wb_fpath
                )
            )
            input()
            wb = load_workbook(wb_fpath)
            sheet = wb[self.pre_consuming_sheet_name]

            f_index = 0
            for row in sheet.iter_rows(
                min_row = row_index_offset,
                min_col = col_index_offset,
                max_row = sheet.max_row,
                max_col = sheet.max_col
            ):
                if f_index > len(foods) -1:
                    break
                food = foods[f_index]
                col_index = self.pre_consuming_sheet_col_index_offset
                for cell in row:
                    if cell.value:
                        cdate = sheet.cell(1,col_index).value
                        food.consumptions.append([
                            datetime.strptime(cdate,"%Y.%m.%d"),
                            float(cell.value)
                        ])
                    col_index += 1
                f_index += 1
            wb.close()
            sheet = None

        pass

    def update_sheets(self):
        pass


# The end.
