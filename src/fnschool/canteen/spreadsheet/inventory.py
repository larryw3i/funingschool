import os
import sys
from fnschool import *
from fnschool.canteen.spreadsheet.base import SpreadsheetBase


class Inventory(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        pass

    def format(self):
        isheet = self.get_inventory_sheet()
        self.unmerge_cells_of_sheet(isheet)

        for row in isheet.iter_rows(
            min_row=1, max_row=isheet.max_row, min_col=1, max_col=9
        ):
            isheet.row_dimensions[row[0].row].height = 14.25

            if row[8].value and "原因" in str(row[8].value).replace(" ", ""):
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row + 1,
                    start_column=9,
                    end_column=9,
                )

            if row[6].value and str(row[6].value).replace(" ", "") == "差额栏":
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=7,
                    end_column=8,
                )

            if row[4].value and str(row[4].value).replace(" ", "") == "盘点栏":
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=5,
                    end_column=6,
                )

            if row[2].value and str(row[2].value).replace(" ", "") == "账面栏":
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=3,
                    end_column=4,
                )

            if row[0].value and row[0].value.replace(" ", "") == "食材名称":
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row + 1,
                    start_column=1,
                    end_column=1,
                )

            if row[0].value and (
                "备注" in row[0].value.replace(" ", "")
                or "审核人" in row[0].value.replace(" ", "")
            ):
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=9,
                )

            if row[0].value and row[0].value.replace(" ", "") == "食材盘存表":
                isheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=9,
                )
                isheet.row_dimensions[row[0].row].height = 22.5

                isheet.merge_cells(
                    start_row=row[0].row + 1,
                    end_row=row[0].row + 1,
                    start_column=1,
                    end_column=9,
                )

    def update(self):
        isheet = self.get_inventory_sheet()
        tnfoods = self.food.get_residue_foods(self.bill.month)
        form_indexes = self.get_inventory_form_indexes()

        for form_index_n in range(0, len(form_indexes)):
            form_index = form_indexes[form_index_n]
            form_index0, form_index1 = form_index
            food_index0 = form_index0 + 3
            food_index1 = form_index1 - 1
            for row in isheet.iter_rows(
                min_row=food_index0,
                max_row=food_index1,
                min_col=1,
                max_col=9,
            ):
                for cell in row:
                    cell.value = ""

        for i, (tn, _foods) in enumerate(tnfoods):
            form_indexes_n = i
            t0, t1 = tn
            form_index = form_indexes[form_indexes_n]
            form_i0, form_i1 = form_index
            fentry_i0 = form_i0 + 3
            fentry_i1 = form_i1 - 1

            self.unmerge_cells_of_sheet(isheet)

            isheet.cell(
                form_i0,
                1,
                f"     "
                + f"学校名称：{self.bill.profile.org_name}"
                + f"                "
                + f"{t1.year} 年 {t1.month} 月 {t1.day} 日"
                + f"              ",
            )

            for row in isheet.iter_rows(
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
                    isheet.cell(row_index + 1, 1).value.replace(" ", "")
                    == "合计"
                ):
                    isheet.insert_rows(row_index + 1, 1)
                isheet.cell(row_index, 1, food.name)
                isheet.cell(row_index, 2, food.unit_name)
                isheet.cell(row_index, 3, food.get_remainder_by_time(tn[1]))
                isheet.cell(
                    row_index,
                    4,
                    food.get_remainder_by_time(tn[1]) * food.unit_price,
                )
                isheet.cell(row_index, 5, food.get_remainder_by_time(tn[1]))
                isheet.cell(
                    row_index,
                    6,
                    food.get_remainder_by_time(tn[1]) * food.unit_price,
                )

        self.format_inventory_sheet()

        wb = self.get_bill_workbook()
        wb.active = isheet
        print_info(_("Sheet '%s' was updated.") % (self.inventory_sheet_name))


# The end.
