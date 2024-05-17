import os
import sys
import random
import calendar
from datetime import datetime, timedelta
import math

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *
from fnschool.canteen.spreadsheet.base import *


class PreConsuming(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.path0 = pre_consuming0_fpath
        self.row_index_offset = 3
        self.col_index_offset = 5

        self.sheet_name0 = self.s.preconsuming_name0

    def pre_consume_foods(self):
        foods = self.bill.foods
        cfoods = [f for f in foods if not f.is_abandoned]
        if len(cfoods) < 1:
            print_error(_("No food found, exit."))
            exit()
        year = self.bill.consuming.year
        month = self.bill.consuming.month
        residual_mark = _("(Remaining)")
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
            tn0_cp = tn0
            if tn0.month != tn1.month:
                tn0 = datetime(tn1.year, tn1.month, 1)
            wb_fpath = (
                self.bill.operator.preconsuming_dpath
                / (
                    _("food_consuming")
                    + "-"
                    + (
                        tn0.strftime("%Y.%m.%d")
                        if not tn0_cp.month == tn1.month
                        else (tn0 + timedelta(days=1)).strftime("%Y.%m.%d")
                    )
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
            tn0_cp = tn0
            if not tn0.month == tn1.month:
                tn0 = datetime(tn1.year, tn1.month, 1)

            wbfoods = [
                f for f in cfoods if f.get_remainder(tn0) > 0 and f.xdate <= tn0
            ]
            for wbfood in [f for f in wbfoods if f.xdate < tn0]:
                if not wbfood.name.endswith(residual_mark):
                    wbfood.name = wbfood.name + residual_mark

            col_index = 0
            for d_index in range(0, (tn1 - tn0).days + 1):
                d_date = tn0 + timedelta(
                    days=d_index + (1 if tn0_cp.month == tn1.month else 0)
                )
                col_index = self.col_index_offset + d_index
                sheet.cell(
                    1,
                    col_index,
                    d_date.strftime("%Y.%m.%d"),
                )
                if d_date == tn1:
                    break

            for col_index in range(col_index + 1, sheet.max_column):
                sheet.cell(1, col_index, "")

            row_index = 0
            for f_index in range(0, len(wbfoods)):
                wbfood = wbfoods[f_index]
                row_index = self.row_index_offset + f_index
                sheet.cell(row_index, 1, wbfood.name)
                sheet.cell(row_index, 2, wbfood.get_remainder(tn0))
                sheet.cell(row_index, 4, wbfood.unit_price)
                if wbfood.name.endswith(residual_mark):
                    wbfood.name = wbfood.name.replace(residual_mark, "")

            for row_index in range(row_index + 1, sheet.max_row + 1):
                sheet.cell(row_index, 1, "")
                sheet.cell(row_index, 2, "")
                sheet.cell(row_index, 4, "")

            wb.save(wb_fpath)
            print_warning(
                _(
                    "Sheet '{0}' of \"{1}\" was updated.\n"
                    + "Press any key to continue when you have "
                    + "completed the foods allocation."
                ).format(sheet.title, wb_fpath)
            )
            new_wbfoods = [
                f for f in cfoods if f.get_remainder(tn1) > 0 and f.xdate == tn1
            ]
            if len(new_wbfoods) > 0:
                print_info(
                    (
                        _("New purchased food for date {0} is:")
                        if len(new_wbfoods) > 1
                        else _("New purchased foods for date {0} are:")
                    ).format(tn1.strftime("%Y.%m.%d"))
                )

                new_wbfoods_count_len = len(str(len(new_wbfoods)))

                number_mark = random.choice([" ", ".", ">", "-", ")", ":", "|"])
                new_wbfood_tips = [
                    (
                        f"{i+1:>{new_wbfoods_count_len}}"
                        + number_mark
                        + f"{f.name} {f.count} {f.unit_name}"
                    )
                    for i, f in enumerate(new_wbfoods)
                ]
                new_wbfood_tips_len = len(new_wbfood_tips)
                new_wbfood_tips_len_sqrt = math.ceil(new_wbfood_tips_len**0.5)
                new_wbfood_tip_len = (
                    max(
                        [
                            len(t) + len([c for c in t if is_zh_CN_char(c)])
                            for t in new_wbfood_tips
                        ]
                    )
                    + 1
                )
                new_wbfood_tips_value = ""
                new_wbfood_tips_col_count = new_wbfood_tips_len_sqrt

                for col_index in range(0, new_wbfood_tips_col_count):
                    col_values = [
                        (i, new_wbfood_tips[i])
                        for i in range(0, new_wbfood_tips_len)
                        if i % new_wbfood_tips_col_count == col_index
                    ]

                    row_len = (
                        max(
                            [
                                len(v)
                                + len([cc for cc in v if is_zh_CN_char(cc)])
                                for i, v in col_values
                            ]
                        )
                        + 1
                    )
                    for i, v in col_values:
                        v_len = row_len - len(
                            [c for c in v if is_zh_CN_char(c)]
                        )
                        new_wbfood_tips[i] = f"{v:<{v_len}}"

                for i, new_wbfood_tip in enumerate(new_wbfood_tips):
                    if i % new_wbfood_tips_col_count == 0 and i != 0:
                        new_wbfood_tips_value += "\n"
                    new_wbfood_tips_value += new_wbfood_tip

                print_warning(new_wbfood_tips_value)

                print_warning(_("Negligible foods are not listed."))
            else:
                print_info(
                    _("There is no purchased food for {0}.").format(
                        tn1.strftime("%Y.%m.%d")
                    )
                )

            print_error(
                _(
                    "There is no need to design for "
                    + "dates without food consumption. "
                    + "(Ok, I know [press any key to continue])"
                )
            )
            input(">_ ")
            wb.close()
            open_file(wb_fpath)
            print_info(
                _(
                    "Ok! I have updated spreadsheet '{0}'. (Press any key)"
                ).format(wb_fpath)
            )
            input(">_ ")
            wb = load_workbook(wb_fpath)
            sheet = wb[self.sheet_name0]

            f_index = 0
            for row in sheet.iter_rows(
                min_row=self.row_index_offset,
                min_col=self.col_index_offset,
                max_row=sheet.max_row,
                max_col=sheet.max_column,
            ):
                if f_index == len(wbfoods):
                    break
                food = wbfoods[f_index]
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
        self.print_consuming_days(cfoods)
        pass

    def print_consuming_days(self, foods):
        consumption_days = []
        year = self.bill.consuming.year
        month = self.bill.consuming.month
        year_month = f"{year}.{month:0>2}"

        for f in foods:
            for d, c in f.consumptions:
                if not d.day in consumption_days:
                    consumption_days.append(d.day)
        consumption_days_value = ""
        space_len = 5
        for week in calendar.monthcalendar(year, month):
            for d in week:
                if d == 0:
                    consumption_days_value += " " * space_len
                elif d in consumption_days:
                    consumption_day = f"({d:>2})"
                    consumption_days_value += f"{consumption_day:>{space_len}}"
                else:
                    d = f" {d:>2} "
                    consumption_days_value += f"{d:>{space_len}}"
            consumption_days_value += "\n"

        print()
        print_error(_("Consuming days of {0}:").format(year_month))
        print_warning(f"{year_month:^{space_len*7}}")
        if consumption_days_value.endswith("\n"):
            consumption_days_value = consumption_days_value[:-1]
        print_info(consumption_days_value[:-1])
        consumption_days_len = len(consumption_days)
        total_days = (
            _("{0} days in total.")
            if consumption_days_len > 1
            else _("{0} day in total.")
        ).format(consumption_days_len)
        print_warning(f"{total_days:^{space_len*7}}")
        print_info(_("Yes, they are all right. (Press any key to continue)"))
        input(">_")
        return


# The end.
