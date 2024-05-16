import os
import sys
import secrets

from fnschool import *
from fnschool.canteen.spreadsheet.base import *


class Food(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = self.s.sfood_name
        pass

    def get_sheet(self, name=None):
        sheet = None
        if name in self.bwb.sheetnames:
            sheet = self.bwb[name]
        else:
            sheet = self.bwb.copy_worksheet(self.bwb[self.sheet_name])
            sheet.title = name
        return sheet

    def format(self, sheet):
        if isinstance(sheet, str):
            sheet = self.get_sheet(sheet)

        self.unmerge_sheet_cells(sheet)

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

        print_info(
            _("Sheet {0} has been reformatted.").format(self.sheet.title)
        )

    def get_form_index(self, sheet):
        indexes = self.get_form_indexes(sheet)
        index_range = indexes[self.bill.consuming.month - 1]
        return index_range

    def get_form_indexes(self, sheet):
        indexes = []
        for row in sheet.iter_rows(
            min_row=1, max_row=sheet.max_row, min_col=1, max_col=14
        ):
            if row[0].value and "材料名称" in str(row[0].value).replace(
                " ", ""
            ):
                indexes.append([row[0].row + 3, None])

            if row[2].value and "合计" in str(row[2].value).replace(" ", ""):
                indexes[-1][1] = row[0].row + 1
        return indexes

    def update(self):

        year = self.bill.consuming.year
        month = self.bill.consuming.month
        cfoods = [f for f in self.bfoods if not f.is_abandoned]
        food_names = list(set([f.name for f in cfoods]))
        wb = self.bwb

        rfoods = [
            f for f in self.bfoods if (not f.is_abandoned and f.is_inventory)
        ]

        food_names = list(set([f.name for f in rfoods] + food_names))

        sheet = None
        for food_name in food_names:
            sheet = self.get_sheet(food_name)
            form_index_range = self.get_form_index(sheet)
            index_start, index_end = form_index_range

            for row_index in range(index_start, index_end - 1):
                for col_index in range(1, 14):
                    sheet.cell(row_index, col_index).value = ""
            row_index = index_start
            col_index = 1

            m_rfoods = [f for f in rfoods if f.name == food_name]
            m_cfoods = [f for f in cfoods if f.name == food_name]

            self.unmerge_sheet_cells(sheet)

            sheet.cell(index_start - 2, 1, f"{year}年")

            if len(m_rfoods) > 0:
                for m_row_index in range(
                    index_start, index_start + len(m_rfoods)
                ):
                    food = m_rfoods[m_row_index - index_start]
                    sheet.cell(
                        m_row_index,
                        3,
                        ("上年结转" if month == 1 else "上月结转"),
                    )
                    sheet.cell(row_index, 10, food.count)
                    sheet.cell(row_index, 11, food.unit_price)
                    sheet.cell(row_index, 12, food.count * food.unit_price)
                    row_index += 1
            else:
                sheet.cell(
                    row_index,
                    3,
                    ("上年结转" if month == 1 else "上月结转"),
                )

                row_index += 1

            cdates = []
            for food in m_cfoods:
                if len(food.consumptions) > 0:
                    cdates += [d for d, c in food.consumptions]
                cdates.append(food.xdate)
            cdates = sorted(list(set(cdates)))

            consuming_n = 1
            warehousing_n = 1
            for cdate in cdates:
                for food in m_cfoods:

                    if food.xdate == cdate and food.xdate.month == month:
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

                    if cdate in [d for d, __ in food.consumptions]:
                        ccount = [
                            c for d, c in food.consumptions if d == cdate
                        ][0]
                        cremainder = food.count - sum(
                            [c for d, c in food.consumptions if d <= cdate]
                        )
                        sheet.cell(row_index, 1, cdate.month)
                        sheet.cell(row_index, 2, cdate.day)
                        sheet.cell(row_index, 6, "")
                        sheet.cell(row_index, 7, ccount)
                        sheet.cell(row_index, 8, food.unit_price)
                        sheet.cell(row_index, 9, ccount * food.unit_price)
                        sheet.cell(row_index, 10, cremainder)
                        sheet.cell(row_index, 11, food.unit_price)
                        sheet.cell(row_index, 12, cremainder * food.unit_price)
                        sheet.cell(
                            row_index,
                            13,
                            f"C{cdate.month:0>2}{consuming_n:0>2}",
                        )
                        consuming_n += 1

                        if "合计" in str(sheet.cell(row_index + 1, 3).value):
                            self.row_inserting_tip(row_index + 1)
                            sheet.insert_rows(row_index + 1, 1)

                        row_index += 1

            self.format(sheet)
            print_info(_("Sheet '%s' was updated.") % sheet.title)

        wb.active = sheet

        bfood_names = list(set([f.name for f in self.bfoods]))
        for name in bfood_names:
            if name in self.bwb.sheetnames:
                sheet = self.get_sheet(name)
                sheet.sheet_properties.tabColor = "0" * 8

        print_info(_("All food sheets have their tab colors reset."))

        for name in food_names:
            sheet = self.get_sheet(name)
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
