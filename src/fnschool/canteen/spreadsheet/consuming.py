from fnschool.canteen.spreadsheet.base import *


class Consuming(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self.sheet_name = self.s.consuming_name
        self.entry_row_len0 = 21
        pass

    @property
    def form_indexes(self):
        if not self._form_indexes:
            csheet = self.sheet
            indexes = []
            row_index = 1
            for row in csheet.iter_rows(max_row=csheet.max_row + 1, max_col=9):
                if row[0].value:
                    if row[0].value.replace(" ", "") == "出库单":
                        indexes.append([row_index + 1, 0])
                    if row[0].value.replace(" ", "") == "合计":
                        indexes[-1][1] = row_index
                row_index += 1

            if len(indexes) > 0:
                self._form_indexes = indexes
            else:
                return None

        return self._form_indexes

    def update(self):
        foods = [f for f in self.bfoods if not f.is_abandoned]
        csheet = self.sheet
        form_indexes = self.form_indexes

        class_names = self.bill.food_class_names

        cdays = []
        for f in foods:
            for d, __ in f.consumptions:
                if not d in cdays:
                    cdays.append(d)
        cdays = sorted(cdays)

        print_info(
            _("Consuming days:")
            + " "
            + " ".join([d.strftime("%Y.%m.%d") for d in cdays])
        )

        merged_ranges = list(csheet.merged_cells.ranges)
        for cell_group in merged_ranges:
            csheet.unmerge_cells(str(cell_group))

        max_day_index = 0
        for day_index in range(0, len(cdays)):
            max_day_index = day_index + 1
            day = cdays[day_index]
            form_index = form_indexes[day_index]
            form_index0, form_index1 = form_index
            food_index0 = form_index0 + 2
            food_index1 = form_index1 - 1
            food_index_len = food_index1 - food_index0 + 1
            tfoods = [
                food
                for food in foods
                if day in [d for d, __ in food.consumptions]
            ]
            tfoods_classes = [f.fclass for f in tfoods]

            classes_without_food = [
                _name for _name in class_names if not _name in tfoods_classes
            ]

            tfoods_len = len(tfoods)
            consuming_n = day_index + 1
            csheet.cell(form_index0, 2, self.purchaser)
            csheet.cell(
                form_index0,
                4,
                f"{day.year}年 {day.month} 月 {day.day} 日  " + f"单位：元",
            )

            csheet.cell(
                form_index0,
                7,
                f"编号：C{day.month:0>2}{consuming_n:0>2}",
            )

            csheet.cell(
                form_index1 + 1,
                1,
                (
                    "   "
                    + "审核人："
                    + "          "
                    + "经办人："
                    + self.operator.name
                    + "　    "
                    + "过称人："
                    + "         "
                    + "仓管人："
                    + " 　      "
                ),
            )

            row_difference = (
                tfoods_len + len(classes_without_food) - food_index_len
            )

            if row_difference > 0:
                self.row_inserting_tip(food_index0 + 1)
                csheet.insert_rows(food_index0 + 1, row_difference)
                form_indexes = self.get_consuming_form_indexes()
                form_index1 += row_difference
                food_index1 += row_difference
                row_difference = 0

            for row in csheet.iter_rows(
                min_row=food_index0,
                max_row=food_index1,
                min_col=1,
                max_col=8,
            ):
                for cell in row:
                    cell.value = ""
                    cell.alignment = self.cell_alignment0
                    cell.border = self.cell_border0

            fentry_index = food_index0

            for class_name in class_names:
                class_foods = [
                    food for food in tfoods if (food.fclass == class_name)
                ]

                fentry_index_start = fentry_index
                if len(class_foods) < 1:
                    csheet.cell(fentry_index_start, 1, class_name)
                    fentry_index = fentry_index_start + 1
                    continue

                class_consuming_count = 0.0
                for food in class_foods:
                    for _date, _count in food.consumptions:
                        if _date == day:
                            class_consuming_count += _count * food.unit_price

                class_foods_len = len(class_foods)
                if class_name == class_names[0] and row_difference < 0:
                    class_foods_len += abs(row_difference) - len(
                        classes_without_food
                    )
                fentry_index_end = fentry_index_start - 1 + class_foods_len

                csheet.cell(fentry_index_start, 1, class_name)
                csheet.cell(fentry_index_start, 7, class_consuming_count)
                csheet.cell(fentry_index_start, 7).number_format = (
                    numbers.FORMAT_NUMBER_00
                )

                for findex, food in enumerate(class_foods):
                    consuming_count = [
                        _count
                        for _date, _count in food.consumptions
                        if _date == day
                    ][0]
                    frow_index = fentry_index_start + findex
                    csheet.cell(frow_index, 2, food.name)
                    csheet.cell(frow_index, 3, food.unit_name)
                    csheet.cell(frow_index, 4, consuming_count)
                    csheet.cell(frow_index, 5, food.unit_price)
                    csheet.cell(
                        frow_index, 6, consuming_count * food.unit_price
                    )
                    csheet.cell(frow_index, 4).number_format = (
                        numbers.FORMAT_NUMBER
                    )
                    csheet.cell(frow_index, 5).number_format = (
                        numbers.FORMAT_NUMBER_00
                    )
                    csheet.cell(frow_index, 6).number_format = (
                        numbers.FORMAT_NUMBER_00
                    )

                fentry_index = fentry_index_end + 1

            tfoods_total_price = 0.0
            for food in tfoods:
                for _date, _count in food.consumptions:
                    if _date == day:
                        tfoods_total_price += _count * food.unit_price
            csheet.cell(form_index1, 6, tfoods_total_price)
            csheet.cell(form_index1, 7, tfoods_total_price)

        if len(form_indexes) > max_day_index:
            for time_index in range(max_day_index, len(form_indexes)):
                form_index0, form_index1 = form_indexes[time_index]
                food_index0, food_index1 = (
                    form_index0 + 2,
                    form_index1 - 1,
                )
                for row in csheet.iter_rows(
                    min_row=food_index0,
                    max_row=food_index1,
                    min_col=2,
                    max_col=7,
                ):
                    for cell in row:
                        cell.value = ""

        self.del_form_empty_row(2)

        self.format()

        wb = self.bwb
        wb.active = csheet
        print_info(_("Sheet '%s' was updated.") % self.sheet.title)

    def format(self):
        csheet = self.sheet
        merged_ranges = list(csheet.merged_cells.ranges)
        for cell_group in merged_ranges:
            csheet.unmerge_cells(str(cell_group))

        for row in csheet.iter_rows(
            min_row=1, max_row=csheet.max_row, min_col=1, max_col=8
        ):
            if row[0].value and row[0].value.replace(" ", "") == "出库单":
                csheet.row_dimensions[row[0].row].height = 21
                csheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=8,
                )
                csheet.merge_cells(
                    start_row=row[0].row + 1,
                    end_row=row[0].row + 1,
                    start_column=4,
                    end_column=6,
                )
                csheet.merge_cells(
                    start_row=row[0].row + 1,
                    end_row=row[0].row + 1,
                    start_column=7,
                    end_column=8,
                )

            if row[0].value and row[0].value.replace(" ", "").endswith("类"):
                row[6].number_format = numbers.FORMAT_NUMBER_00
                for _row in csheet.iter_rows(
                    min_row=row[0].row + 1,
                    max_row=csheet.max_row + 1,
                    min_col=1,
                    max_col=1,
                ):
                    if _row[0].value and (
                        _row[0].value.replace(" ", "").endswith("类")
                        or _row[0].value.replace(" ", "") == "合计"
                    ):
                        csheet.merge_cells(
                            start_row=row[0].row,
                            end_row=_row[0].row - 1,
                            start_column=1,
                            end_column=1,
                        )
                        csheet.merge_cells(
                            start_row=row[0].row,
                            end_row=_row[0].row - 1,
                            start_column=7,
                            end_column=7,
                        )
                        break

            if row[0].value and "审核人" in row[0].value.replace(" ", ""):
                csheet.merge_cells(
                    start_row=row[0].row,
                    end_row=row[0].row,
                    start_column=1,
                    end_column=8,
                )

        wb = self.bwb
        wb.active = csheet

        print_info(_("Sheet '%s' was formatted.") % self.sheet.title)


# The end.
