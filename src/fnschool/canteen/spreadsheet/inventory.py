import os
import sys
import calendar
from datetime import datetime
from fnschool import *
from fnschool.canteen.spreadsheet.base import SpreadsheetBase


class Inventory(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = "食材盘存表"
        pass

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

        print_info(
            _("Sheet \"{0}\" has been reformatted.").format(sheet.title)
        )

    @property
    def form_indexes(self):
        sheet = self.sheet
        indexes = []
        row_index = 1
        for row in sheet.iter_rows(max_row=sheet.max_row + 1, max_col=8):
            if row[0].value:
                if row[0].value.replace(" ", "") == "食材盘存表":
                    indexes.append([row_index + 1, 0])
                if row[0].value.replace(" ", "") == "合计":
                    indexes[-1][1] = row_index
            row_index += 1

        if len(indexes) > 0:
            return indexes

        return None

    @property
    def foods(self):
        foods = []
        bfoods = [ f for f in self.bfoods if not f.is_abandoned]
        year = bfoods[-1].xdate.year
        month = bfoods[-1].xdate.month

        consuming_dates = []
        for bfood in bfoods:
            for d,__ in bfood.consumptions:
                consuming_dates.append(d)
        consuming_dates = list(set(consuming_dates))

        for tn in calendar.monthcalendar(year,month):
            if 0 in tn:
                tn = list(set(tn))
                tn.remove(0)
            tn0,tn1 = tn[0],tn[-1]
            for d in range(tn1,tn0-1,-1):
                d_date = datetime(year,month,d)
                if d_date in consuming_dates:
                    foods.append([d_date, [f for f in bfoods if f.get_remainder(d_date)]])
                    break
        return foods
            

    def update(self):
        sheet = self.sheet
        tnfoods = self.foods
        for tn1, foods in tnfoods:
            print(tn1,[(f.name,f.get_remainder(tn1)) for f in foods])
        form_indexes = self.form_indexes

        self.unmerge_sheet_cells()

        for form_index_n in range(0, len(form_indexes)):
            form_index = form_indexes[form_index_n]
            form_index0, form_index1 = form_index
            food_index0 = form_index0 + 3
            food_index1 = form_index1 - 1
            for row in sheet.iter_rows(
                min_row=food_index0,
                max_row=food_index1,
                min_col=1,
                max_col=9,
            ):
                for cell in row:
                    cell.value = ""

        for i, (t1, _foods) in enumerate(tnfoods):
            form_indexes_n = i
            form_index = form_indexes[form_indexes_n]
            form_i0, form_i1 = form_index
            fentry_i0 = form_i0 + 3
            fentry_i1 = form_i1 - 1


            sheet.cell(
                form_i0,
                1,
                f"     "
                + f"学校名称：{self.purchaser}"
                + f"                "
                + f"{t1.year} 年 {t1.month} 月 {t1.day} 日"
                + f"              ",
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
                if (
                    sheet.cell(row_index + 1, 1).value.replace(" ", "")
                    == "合计"
                ):
                    sheet.insert_rows(row_index + 1, 1)
                sheet.cell(row_index, 1, food.name)
                sheet.cell(row_index, 2, food.unit_name)
                sheet.cell(row_index, 3, food.get_remainder(t1))
                sheet.cell(
                    row_index,
                    4,
                    food.get_remainder(t1) * food.unit_price,
                )
                sheet.cell(row_index, 5, food.get_remainder(t1))
                sheet.cell(
                    row_index,
                    6,
                    food.get_remainder(t1) * food.unit_price,
                )

        self.format()

        wb = self.bwb
        wb.active = sheet
        print_info(_("Sheet '%s' was updated.") % (self.sheet_name))


# The end.
