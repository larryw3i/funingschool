import os
import sys

from fnschool import *
from fnschool.canteen.spreadsheet.base import SpreadsheetBase


class Food(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        pass

    def format(self, sheet):
        if isinstance(sheet, str):
            sheet = self.get_food_sheet(sheet)
        self.unmerge_cells_of_sheet(sheet)
        for row in sheet.iter_rows(
            min_row=1,
            max_row=sheet.max_row,
            min_col=1,
            max_col=14,
        ):
            sheet.row_dimensions[row[0].row].height = 15.75
            if row[0].value and "入库、出库台账" in str(row[0].value):
                sheet.row_dimensions[row[0].row].height = 27
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=13,
                )

            if row[0].value and "年" in str(row[0].value):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=2,
                )

            if row[3].value and "入库" in str(row[3].value).replace(
                " ", ""
            ).replace("　", ""):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=4,
                    end_column=6,
                )

            if row[6].value and "出库" in str(row[6].value).replace(
                " ", ""
            ).replace("　", ""):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=7,
                    end_column=9,
                )

            if row[9].value and "库存" in str(row[9].value).replace(
                " ", ""
            ).replace("　", ""):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=10,
                    end_column=12,
                )

            if row[12].value and "编号" in str(row[12].value).replace(" ", ""):
                sheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row + 1,
                    start_column=13,
                    end_column=13,
                )

    def update(self):
        time_nodes = sorted(
            [
                tn
                for tn in self.bill.get_time_nodes()
                if tn[1].month == self.bill.month
            ]
        )
        time_nodes_mm1 = sorted(
            [
                tn
                for tn in self.bill.get_time_nodes()
                if tn[1].month == self.bill.month - 1
            ]
        )
        t0, t1 = time_nodes[-1]
        cfoods = [
            f
            for f in self.food.get_foods()
            if (
                (
                    f.xdate.month == self.bill.month
                    or (
                        self.bill.month
                        in [d.month for d, c in f.consuming_list]
                    )
                )
                and not f.is_negligible
            )
        ]
        food_names = list(set([f.name for f in cfoods]))
        wb = self.get_bill_workbook()
        tn0_dm1 = (
            (time_nodes[0][0] + timedelta(days=-1))
            if len(time_nodes_mm1) < 1
            else (time_nodes_mm1[-1][1])
        )

        rfoods = [
            f
            for f in self.food.get_foods()
            if (
                f.get_remainder_by_time(tn0_dm1) > 0
                and not f.is_negligible
                and f.xdate.month < self.bill.month
            )
        ]

        food_names = list(set([f.name for f in rfoods] + food_names))

        sheet = None
        for food_name in food_names:
            sheet = self.get_food_sheet(food_name)
            form_index_range = self.get_food_form_index(sheet)
            index_start, index_end = form_index_range

            for row_index in range(index_start, index_end - 1):
                for col_index in range(1, 14):
                    sheet.cell(row_index, col_index).value = ""
            row_index = index_start
            col_index = 1

            _rfoods = [f for f in rfoods if f.name == food_name]
            _cfoods = [f for f in cfoods if f.name == food_name]

            self.unmerge_cells_of_sheet(sheet)

            sheet.cell(index_start - 2, 1, f"{t1.year}年")

            if len(_rfoods) > 0:
                for _row_index in range(
                    index_start, index_start + len(_rfoods)
                ):
                    food = _rfoods[_row_index - index_start]
                    sheet.cell(
                        _row_index,
                        3,
                        ("上年结转" if t1.month == 1 else "上月结转"),
                    )
                    sheet.cell(row_index, 10, food.count)
                    sheet.cell(row_index, 11, food.unit_price)
                    sheet.cell(row_index, 12, food.count * food.unit_price)
                    row_index += 1
            else:
                sheet.cell(
                    row_index,
                    3,
                    ("上年结转" if t1.month == 1 else "上月结转"),
                )

                row_index += 1

            _cdates = []
            for food in _cfoods:
                if len(food.consuming_list) > 0:
                    _cdates += [d for d, c in food.consuming_list]
                _cdates.append(food.xdate)
            _cdates = [d for d in _cdates if d.month == self.bill.month]
            _cdates = sorted(list(set(_cdates)))

            consuming_n = 1
            warehousing_n = 1
            for cdate in _cdates:
                for food in _cfoods:

                    if food.xdate == cdate:
                        sheet.cell(row_index, 1, cdate.month)
                        sheet.cell(row_index, 2, cdate.day)
                        sheet.cell(row_index, 4, food.count)
                        sheet.cell(row_index, 5, food.unit_price)
                        sheet.cell(row_index, 6, food.count * food.unit_price)
                        sheet.cell(row_index, 9, "")
                        sheet.cell(row_index, 10, food.count)
                        sheet.cell(row_index, 11, food.unit_price)
                        sheet.cell(row_index, 12, food.count * food.unit_price)
                        sheet.cell(
                            row_index,
                            13,
                            f"R{cdate.month:0>2}{warehousing_n:0>2}",
                        )
                        warehousing_n += 1

                        if "合计" in str(sheet.cell(row_index + 1, 3).value):
                            sheet.insert_rows(row_index + 1, 1)

                        row_index += 1

                    if cdate in [d for d, __ in food.consuming_list]:
                        _count = [
                            c for d, c in food.consuming_list if d == cdate
                        ][0]
                        _remainder = food.count - sum(
                            [c for d, c in food.consuming_list if d <= cdate]
                        )
                        sheet.cell(row_index, 1, cdate.month)
                        sheet.cell(row_index, 2, cdate.day)
                        sheet.cell(row_index, 6, "")
                        sheet.cell(row_index, 7, _count)
                        sheet.cell(row_index, 8, food.unit_price)
                        sheet.cell(row_index, 9, _count * food.unit_price)
                        sheet.cell(row_index, 10, _remainder)
                        sheet.cell(row_index, 11, food.unit_price)
                        sheet.cell(row_index, 12, _remainder * food.unit_price)
                        sheet.cell(
                            row_index,
                            13,
                            f"C{cdate.month:0>2}{consuming_n:0>2}",
                        )
                        consuming_n += 1

                        if "合计" in str(sheet.cell(row_index + 1, 3).value):
                            sheet.insert_rows(row_index + 1, 1)

                        row_index += 1

            self.format_food_sheet(sheet)
            print_info(_("Sheet '%s' was updated.") % sheet.title)

        wb.active = sheet

        _food_names = list(set([f.name for f in self.food.get_foods()]))
        for name in _food_names:
            if self.includes_sheet(name):
                sheet = self.get_bill_sheet(name)
                sheet.sheet_properties.tabColor = "0" * 8

        print_info(_("All food sheets have their tab colors reset."))

        for name in food_names:
            sheet = self.get_food_sheet(name)
            sheet.sheet_properties.tabColor = secrets.token_hex(4)

        print_info(
            _("Food sheets [{0}] have their tab colors recolor.").format(
                " ".join(food_names)
            )
        )
        print_info(
            _("Food sheets [{0}] have been updated.").format(
                " ".join(food_names)
            )
        )


# The end
