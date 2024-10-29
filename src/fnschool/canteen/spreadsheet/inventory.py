import os
import sys
import re
import calendar
from datetime import datetime
from fnschool import *
from fnschool.canteen.food import Food
from fnschool.canteen.spreadsheet.base import *


class Inventory(Base):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = self.s.inventory_name
        self.entry_row_len0 = 17
        pass

    def get_entry_index(self, form_index):
        form_index0, form_index1 = form_index
        entry_index = [form_index0 + 4, form_index1 - 3]
        return entry_index

    def format(self):
        sheet = self.sheet
        self.unmerge_sheet_cells(sheet)

        for row in sheet.iter_rows(
            min_row=1, max_row=sheet.max_row, min_col=1, max_col=9
        ):
            sheet.row_dimensions[row[0].row].height = 14.25

            if row[8].value and "原因" in str(row[8].value).replace(" ", ""):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row + 1,
                    start_column=9,
                    end_column=9,
                )

            if row[6].value and str(row[6].value).replace(" ", "") == "差额栏":
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=7,
                    end_column=8,
                )

            if row[4].value and str(row[4].value).replace(" ", "") == "盘点栏":
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=5,
                    end_column=6,
                )

            if row[2].value and str(row[2].value).replace(" ", "") == "账面栏":
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=3,
                    end_column=4,
                )

            if row[0].value and row[0].value.replace(" ", "") == "食材名称":
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row + 1,
                    start_column=1,
                    end_column=1,
                )

            if row[0].value and (
                "备注" in row[0].value.replace(" ", "")
                or "审核人" in row[0].value.replace(" ", "")
            ):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=9,
                )

            if row[0].value and row[0].value.replace(" ", "") == "食材盘存表":
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=9,
                )
                sheet.row_dimensions[row[0].row].height = 22.5

                sheet.merge_cells(
                    start_row=row[0].row + 1,
                    end_row=row[0].row + 1,
                    start_column=1,
                    end_column=9,
                )

        print_info(_('Sheet "{0}" has been reformatted.').format(sheet.title))

    @property
    def form_indexes(self):
        if not self._form_indexes:
            sheet = self.sheet
            indexes = []
            for row in sheet.iter_rows(max_row=sheet.max_row + 1, max_col=8):
                if row[0].value:
                    cell0_value = str(row[0].value).replace(" ", "")
                    if "食材盘存表" in cell0_value:
                        indexes.append([row[0].row, 0])
                    if "审核人" in cell0_value:
                        indexes[-1][1] = row[0].row

            self._form_indexes = indexes

        return self._form_indexes

    @property
    def saved_foods(self):
        _foods = self.get_save_foods()
        return _foods

    def get_save_foods(self, meal_type=None):
        bill_fpath = self.bill.operator.get_bill_fpath(meal_type)
        wb = load_workbook(bill_fpath, read_only=True)
        sheet = wb[self.sheet_name]
        purchasing = self.bill.spreadsheet.purchasing

        food_index_m1 = []

        for row_index in range(1, sheet.max_row):
            if "食材名称" in str(sheet.cell(row_index, 1).value):
                if sheet.cell(row_index + 2, 1).value:
                    food_index_m1 = [row_index + 2, None]
                else:
                    break
            if "合计" in str(sheet.cell(row_index, 1).value):
                food_index_m1[1] = row_index - 1

        if len(food_index_m1) < 1:
            return []

        foods = []
        header_info = str(sheet.cell(food_index_m1[0] - 3, 1).value)
        header_info0 = header_info.replace(" ", "")

        purchaser = re.split(r"\d+", re.split(r"：\s*", header_info0)[1])[0]
        year = int(
            re.split(r"\D+", re.split(r"年", header_info0)[0].strip())[-1]
        )
        month = int(re.split(r"月", re.split(r"年", header_info0)[-1])[0])
        day = int(re.split(r"月", re.split(r"日", header_info0)[0])[-1])

        for row_index in range(food_index_m1[0], food_index_m1[1] + 1):
            fname = sheet.cell(row_index, 1).value
            if not fname:
                break
            funit_name = sheet.cell(row_index, 2).value or _("No unit")
            fcount = float(sheet.cell(row_index, 5).value)
            ftotal_price = float(sheet.cell(row_index, 6).value)

            food = Food(
                self.bill,
                name=fname,
                unit_name=funit_name,
                fclass=purchasing.get_food_class(fname),
                count=fcount,
                total_price=ftotal_price,
                xdate=f"{year}-{month}-{day}",
                purchaser=purchaser,
                is_inventory=True,
                is_abandoned=False,
            )
            foods.append(food)
        if len(foods) < 1:
            return None
        return foods

    @property
    def foods(self):
        foods = []
        bfoods = [f for f in self.bfoods if not f.is_abandoned]
        year = self.bill.consuming.year
        month = self.bill.consuming.month

        consuming_dates = []
        for bfood in bfoods:
            for d, __ in bfood.consumptions:
                consuming_dates.append(d)
        consuming_dates = list(set(consuming_dates))

        for tn in calendar.monthcalendar(year, month):
            if 0 in tn:
                tn = list(set(tn))
                tn.remove(0)
            tn0, tn1 = tn[0], tn[-1]
            for d in range(tn1, tn0 - 1, -1):
                d_date = datetime(year, month, d)
                if d_date in consuming_dates:
                    foods.append(
                        [
                            d_date,
                            [
                                f
                                for f in bfoods
                                if (
                                    f.get_remainder(d_date) > 0
                                    and f.xdate != d_date
                                )
                            ],
                        ]
                    )
                    break
        ifoods = [f for f in bfoods if f.is_inventory]
        if len(ifoods) > 0:
            foods = [[ifoods[0].xdate, ifoods]] + foods
        return foods

    def update(self):
        sheet = self.sheet
        tnfoods = self.foods
        form_indexes = self.form_indexes
        self.unmerge_sheet_cells()

        for form_index_n in range(0, len(form_indexes)):
            form_index = form_indexes[form_index_n]
            form_index0, form_index1 = form_index
            food_index0, food_index1 = self.get_entry_index(form_index)
            for row in sheet.iter_rows(
                min_row=food_index0,
                max_row=food_index1,
                min_col=1,
                max_col=9,
            ):
                for cell in row:
                    cell.value = ""

        for i, (t1, _foods) in enumerate(tnfoods):

            if len(_foods) < 1:
                print_warning(
                    _('There is no inventories for "{0}".').format(
                        t1.strftime("%Y-%m-%d")
                    )
                )
                continue

            form_indexes_n = i
            form_index = form_indexes[form_indexes_n]
            form_i0, form_i1 = form_index
            fentry_i0, fentry_i1 = self.get_entry_index(form_index)

            sheet.cell(
                form_i0 + 1,
                1,
                f"     "
                + f"学校名称：{self.purchaser}"
                + f"                "
                + f"{t1.year} 年 {t1.month} 月 {t1.day} 日"
                + f"              ",
            )
            sheet.cell(
                form_i1,
                1,
                (
                    "   "
                    + "审核人："
                    + "        "
                    + "经办人："
                    + self.operator.name
                    + "　    "
                    + "过称人："
                    + "        "
                    + "仓管人："
                    + " 　     "
                ),
            )

            for row in sheet.iter_rows(
                min_row=fentry_i0,
                max_row=fentry_i1,
                min_col=1,
                max_col=9,
            ):
                for cell in row:
                    cell.value = ""
                    cell.alignment = self.cell_alignment0
                    cell.border = self.cell_border0

            for findex, food in enumerate(_foods):
                row_index = fentry_i0 + findex
                if sheet.cell(row_index + 1, 1).value and (
                    sheet.cell(row_index + 1, 1).value.replace(" ", "")
                    == "合计"
                ):
                    i_row_index = row_index + 1
                    self.row_inserting_tip(i_row_index)
                    sheet.insert_rows(i_row_index, 1)

                    for i_col_index in range(1, 10):
                        cell = sheet.cell(i_row_index, i_col_index)
                        cell.alignment = self.cell_alignment0
                        cell.border = self.cell_border0

                    self.del_form_indexes()
                    form_indexes = self.form_indexes
                unit_price = food.unit_price
                sheet.cell(row_index, 1, food.name)
                sheet.cell(row_index, 2, food.unit_name)
                sheet.cell(row_index, 3, food.get_remainder(t1))
                sheet.cell(
                    row_index,
                    4,
                    food.get_remainder(t1) * unit_price,
                )
                sheet.cell(row_index, 5, food.get_remainder(t1))
                sheet.cell(
                    row_index,
                    6,
                    food.get_remainder(t1) * unit_price,
                )

        self.del_form_empty_rows([1])
        self.format()

        wb = self.bwb
        wb.active = sheet
        print_info(_("Sheet '%s' was updated.") % (self.sheet_name))


# The end.
