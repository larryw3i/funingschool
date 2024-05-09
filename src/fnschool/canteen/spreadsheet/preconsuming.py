
import os
import sys
import calendar
from datetime import datetime, timedelta

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *
from fnschool.canteen.spreadsheet.base import *

class PreConsuming(SpreadsheetBase):
    def __init__(self,bill):
        super().__init__(bill)
        self.path0 = pre_consuming0_fpath
        self.row_index_offset = 3
        self.col_index_offset = 5
 
        self.sheet_name0 = "出库计划表"

    def pre_consume_foods(self, foods):
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

        wb_fpathes = []
        for i in range(1, len(time_nodes)):
            tn0, tn1 = time_nodes[i - 1], time_nodes[i]
            if tn0.month != tn1.month:
                tn0 = datetime(tn1.year, tn1.month, 1)
            wb_fpath = (
                self.bill.operator.preconsuming_dpath
                / (
                    f"consuming-"
                    + tn0.strftime("%Y.%m.%d")
                    + "-"
                    + tn1.strftime("%Y.%m.%d")
                    + ".xlsx"
                )
            ).as_posix()

            wb_fpathes.append(wb_fpath)

        for i, wb_fpath in enumerate(wb_fpathes):
            if not Path(wb_fpath).exists():
                shutil.copy(self.path0, wb_fpath)
                print_info(
                    _('Spreadsheet "{0}" was copied to "{1}".').format(
                        self.path0, wb_fpath
                    )
                )
            wb = load_workbook(wb_fpath)
            sheet = wb[self.sheet_name0]
            tn1 = time_nodes[i + 1]
            tn0 = time_nodes[i]
            if not tn0.month == tn1.month:
                tn0 = datetime(tn1.year, tn1.month, 1)


            wbfoods = [f for f in cfoods if f.get_remmainer(tn0) > 0 and f.xdate <= tn0]
            for wbfood in [f for f in wbfoods if f.xdate < tn0]:
                residual_mark = _("(Remaining)")
                if not wbfood.name.endswith(residual_mark):
                    wbfood.name = wbfood.name + residual_mark
            
            col_index = 0
            for d_index in range(0, (tn1 - tn0).days + 1):
                d_date = tn0 + timedelta(days=d_index)
                col_index = self.col_index_offset + d_index
                sheet.cell(
                    1,
                    col_index,
                    d_date.strftime("%Y.%m.%d"),
                )

            for col_index in range(col_index+1,sheet.max_column):
                    sheet.cell(1,col_index,'')
            
            row_index = 0
            for f_index in range(0, len(wbfoods)):
                wbfood = wbfoods[f_index]
                row_index = self.row_index_offset + f_index
                sheet.cell(row_index, 1, wbfood.name)
                sheet.cell(row_index, 2, wbfood.get_remmainer(tn0))
                sheet.cell(row_index, 4, wbfood.unit_price)

            for row_index in range(row_index+1,sheet.max_row+1):
                sheet.cell(row_index, 1, "")
                sheet.cell(row_index, 2, "")
                sheet.cell(row_index, 4, "")



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
                _(
                    "Ok! I have updated spreadsheet '{0}'. (Press any key)"
                ).format(wb_fpath)
            )
            input()
            wb = load_workbook(wb_fpath)
            sheet = wb[self.sheet_name0]

            f_index = 0
            for row in sheet.iter_rows(
                min_row=self.row_index_offset,
                min_col=self.col_index_offset,
                max_row=sheet.max_row,
                max_col=sheet.max_column,
            ):
                if f_index > len(foods) - 1:
                    break
                food = foods[f_index]
                col_index = self.col_index_offset
                for cell in row:
                    if cell.value:
                        cdate = sheet.cell(1, col_index).value
                        food.consumptions.append(
                            [
                                datetime.strptime(cdate, "%Y.%m.%d"),
                                float(cell.value),
                            ]
                        )
                    col_index += 1
                f_index += 1
            wb.close()
            sheet = None

        pass


# The end.