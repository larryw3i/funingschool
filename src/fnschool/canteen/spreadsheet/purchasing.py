import os
import sys
from openpyxl.utils.cell import get_column_letter
import tomllib
from tkinter import filedialog
from fnschool import *
from fnschool.canteen.path import *
from fnschool.canteen.food import *
from fnschool.canteen.spreadsheet.base import *
from openpyxl.worksheet.datavalidation import DataValidation


class Purchasing(SpreadsheetBase):
    def __init__(self, bill):
        super().__init__(bill)
        self._path = None
        self._food_name_col = [
            None,
            None,
            ["商品名称", "食材名称", "食品名称"],
        ]
        self._unit_name_col = [
            None,
            None,
            ["订货单位", "食材单位", "订购单位", "计量单位"],
        ]
        self._total_price_col = [
            None,
            None,
            ["总价", "折前金额", "折后金额", "总金额"],
        ]
        self._xdate_col = [
            None,
            None,
            ["送货日期", "检查日期", "清点日期", "x日期", "日期"],
        ]
        self._purchaser_col = [
            None,
            None,
            [
                "客户名称",
                "购买者",
                "购买者名称",
                "顾客名称",
                "下单单位名",
                "购入单位名",
            ],
        ]
        self._count_col = [
            None,
            None,
            ["总数", "数量", "下单数量", "订货数量", "发货数量"],
        ]
        self._abandoned_col = [
            None,
            None,
            [
                "不计",
                "是不计",
                "未入库",
                "非入库",
                "不需入库",
                "是非入库",
            ],
        ]
        self._inventory_col = [
            None,
            None,
            [
                "盘存",
                "存余",
                "结余",
                "是结余",
                "剩余",
                "是剩余",
                "是盘存",
            ],
        ]

        self._food_class_col = [
            "食材大类",
            None,
            ["食材大类", "大类", "食材分类", "食材主类"],
        ]
        self._wb = None
        self._sheet = None
        self._headers = None

    def get_col(self, col):
        if not col[1]:
            col0 = [
                (n, self.headers.index(n) + 1)
                for n in self.headers
                if n in col[2]
            ][-1]
            col[0] = col0[0]
            col[1] = col0[1]
        return col

    @property
    def xdate_col(self):
        return self.get_col(self._xdate_col)

    @property
    def purchaser_col(self):
        return self.get_col(self._purchaser_col)

    @property
    def food_name_col(self):
        return self.get_col(self._food_name_col)

    @property
    def food_class_col(self):
        return self.get_col(self._food_class_col)

    @property
    def unit_name_col(self):
        return self.get_col(self._unit_name_col)

    @property
    def count_col(self):
        return self.get_col(self._count_col)

    @property
    def total_price_col(self):
        return self.get_col(self._total_price_col)

    @property
    def abandoned_col(self):
        return self.get_col(self._abandoned_col)

    @property
    def inventory_col(self):
        return self.get_col(self._inventory_col)

    @wb.deleter
    def wb(self):
        del self._wb

    @property
    def wb(self):
        if not self._wb:
            print_info(_('Loading data from "{0}".').format(self.path))
            self._wb = load_workbook(self.path)
        return self._wb

    @property
    def sheet(self):
        if not self._sheet:
            self._sheet = self.wb.active
        return self._sheet

    @property
    def headers(self):
        if not self._headers:
            self._headers = [
                v
                for v in [
                    self.sheet.cell(1, col_index).value
                    for col_index in range(1, self.sheet.max_column + 1)
                ]
                if v
            ]
        return self._headers

    def add_class_col(self):
        if not any(
            [fclass in self.headers for fclass in self.food_class_col[2]]
        ):
            fname_col_index = (
                max(
                    [
                        self._headers.index(n)
                        for n in self._headers
                        if n in self._food_name_col[2]
                    ]
                )
                + 1
            )
            fclass_col_index = fname_col_index + 1
            self.sheet.insert_cols(fclass_col_index, 1)
            self.sheet.cell(1, fclass_col_index, self._food_class_col[0])
            for row_index in range(2, self.sheet.max_row + 1):
                fname = self.sheet.cell(row_index, fname_col_index).value
                if not fname:
                    break
                self.sheet.cell(
                    row_index, fclass_col_index, self.get_food_class(fname)
                )
            self.wb.save(self.path)
            self.wb.close()
            del self.wb
            print_info(
                _(
                    'Column "{0}" has been updated, '
                    + "feel free to open new issue if some "
                    + "food with the wrong class ({1}). "
                ).format(self._food_class_col[0], get_new_issue_url())
            )
            print_warning(
                _(
                    "Ok, I'd like to check and update it. "
                    + "(Press any key to check the file)"
                )
            )
            input()
            open_path(self.path)
            print_info(
                _(
                    "I have checked it, and all classes of "
                    + "food are right. (Press any key to continue)"
                )
            )

    @property
    def food_classes(self):
        food_classes = self.bill.food_classes
        return food_classes

    def food_name_like(self, name, like):
        not_likes = None
        if "!" in like:
            like = like.split("!")
            not_likes = like[1:]
            like = like[0]

        result = None
        like_value = like.replace("*", "")
        if like.startswith("*") and not like.endswith("*"):
            result = name.endswith(like_value)
        elif like.endswith("*") and not like.startswith("*"):
            result = name.startswith(like_value)
        elif not "*" in like:
            result = like_value == name
        elif like.startswith("*") and like.endswith("*"):
            result = like_value in name

        if not_likes:
            result = result and not any(
                [self.food_name_like(name, nl) for nl in not_likes]
            )
        return result
        pass

    def get_food_class(self, name):
        food_classes = self.food_classes
        for fclass, name_likes in food_classes.items():
            for name_like in name_likes:
                if self.food_name_like(name, name_like):
                    return fclass
        return "蔬菜类"

    @property
    def path(self):
        if not self._path:
            print_info(
                _(
                    "{0} need a purchasing list file, "
                    + "and it's file type should be '.xlsx'. "
                    + "The column names of it:"
                ).format(app_name)
                + _(
                    ""
                    + "\n\tcolumn   type    example"
                    + "\n\t送货日期 Text    2024-03-01"
                    + "\n\t食材名称 Text    香菜"
                    + "\n\t数量     Number  20"
                    + "\n\t计量单位 Text    斤"
                    + "\n\t总价     Number  20.0"
                    + "\n\t购买者   Text    "
                    + "\n\t是不计   Text    y"
                    + "\n\t是结余   Text    y"
                )
            )
            print_info(_("Please select a purchasing file."))
            filetypes = ((_("Spreadsheet Files"), "*.xlsx"),)

            filename = filedialog.askopenfilename(
                title=_("Please select the purchasing file"),
                initialdir=(Path.home() / "Downloads").as_posix(),
                filetypes=filetypes,
            )
            if filename is None or filename == ():
                print_warning(_("No file was selected, exit."))
                exit()
                return None
            print_info(
                _('Purchasing list file "{0}" has been selected.').format(
                    filename
                )
            )
            self._path = filename
        return self._path

    def update(self):
        self.add_class_col()
        self.update_inventories()

    def update_inventories(self):

        merged_ranges = list(self.sheet.merged_cells.ranges)
        for cell_group in merged_ranges:
            sheet.unmerge_cells(str(cell_group))

        inventories_len = len(
            [
                row_index
                for row_index in range(2, self.sheet.max_row + 1)
                if self.sheet.cell(row_index, self.inventory_col[1]).value
            ]
        )

        if inventories_len < 1:
            print_warning(
                _("The remaining food wasn't read " + 'from "{0}".').format(
                    self.path,
                )
            )
            inventory = self.bill.spreadsheet.inventory
            print_info(
                _(
                    "{0} is reading remaining foods from "
                    + 'Sheet "{1}" of Spreadsheet "{2}" ......'
                ).format(
                    app_name,
                    inventory.sheet_name,
                    self.bill.operator.bill_fpath,
                )
            )
            saved_ifoods = inventory.saved_foods
            saved_ifoods_len = len(saved_ifoods)
            if saved_ifoods:
                print_warning(
                    (
                        _(
                            "Some remaining foods have been read "
                            + 'from sheet "{0}" of spreadsheet "{1}":'
                        )
                        if len(saved_ifoods) > 1
                        else _(
                            "The remaining food has been read"
                            + 'from sheet "{0}" of spreadsheet "{1}":'
                        )
                    ).format(inventory.sheet_name, self.operator.bill_fpath)
                )

                saved_ifoods_len2 = len(str(saved_ifoods_len))
                saved_ifoods_s = sqr_slist(
                    [
                        (
                            f"({i+1:>{saved_ifoods_len2}}) {f0.name}:{f0.count} {f0.unit_name}"
                            + f"\u2a09 {f0.unit_price:.2f} {self.bill.currency.unit}/"
                            + f"{f0.unit_name}={f0.total_price:.2f} "
                            + f"{self.bill.currency.unit}"
                        )
                        for i, f0 in enumerate(saved_ifoods)
                    ]
                )

                print_info(saved_ifoods_s)
                print_warning(
                    (
                        _('Fill them in "{0}"? (YyNn)')
                        if len(saved_ifoods) > 1
                        else _('Fill it in "{0}" (YyNn)')
                    ).format(self.path)
                )

                f_input = input(">_ ").replace(" ", "")
                if f_input in "Yy":
                    max_row = len(
                        [
                            row_index
                            for row_index in range(1, self.sheet.max_row + 1)
                            if self.sheet.cell(row_index, 1).value
                        ]
                    )
                    for row_index in range(
                        max_row + 1, max_row + 1 + len(saved_ifoods)
                    ):
                        f = saved_ifoods[row_index - max_row - 1]
                        self.sheet.cell(
                            row_index, self.xdate_col[1]
                        ).number_format = numbers.FORMAT_TEXT
                        self.sheet.cell(
                            row_index,
                            self.xdate_col[1],
                            f.xdate.strftime("%Y-%m-%d"),
                        )
                        self.sheet.cell(
                            row_index, self.purchaser_col[1], f.purchaser
                        )
                        self.sheet.cell(
                            row_index, self.food_name_col[1], f.name
                        )
                        self.sheet.cell(
                            row_index, self.food_class_col[1], f.fclass
                        )
                        self.sheet.cell(
                            row_index,
                            self.unit_name_col[1],
                            f.unit_name,
                        )
                        self.sheet.cell(
                            row_index, self.count_col[1]
                        ).number_format = numbers.FORMAT_NUMBER_00
                        self.sheet.cell(row_index, self.count_col[1], f.count)
                        self.sheet.cell(
                            row_index, self.total_price_col[1]
                        ).number_format = numbers.FORMAT_NUMBER_00
                        self.sheet.cell(
                            row_index, self.total_price_col[1], f.total_price
                        )
                        self.sheet.cell(row_index, self.inventory_col[1], "y")

                    print_info(
                        (
                            _('The remaining foods have been added to "{0}".')
                            if len(saved_ifoods) > 1
                            else _(
                                'The remaining food has been added to "{0}".'
                            )
                        ).format(self.path)
                    )
                    self.wb.save(self.path)
                    self.wb.close()
                    print_info(
                        (
                            _(
                                "Please check/modify the updated data. "
                                + "(Press any key to open the file)"
                            )
                        )
                    )
                    input(">_ ")
                    open_path(self.path)
                    print_info(
                        _(
                            "Ok, I checked it, it's ok. (Press any key to continue)"
                        )
                    )
                    input(">_ ")
        pass

    def read_pfoods(self):
        self.update()
        foods = pd.read_excel(self.path)
        self.set_col_names(foods.columns)
        _foods = []
        for __, food in foods.iterrows():
            _food = Food(
                self.bill,
                name=food[self.food_name_col[0]],
                unit_name=food[self.unit_name_col[0]],
                count=food[self.count_col[0]],
                total_price=food[self.total_price_col[0]],
                xdate=food[self.xdate_col[0]],
                purchaser=food[self.purchaser_col[0]],
                fclass=food[self.food_class_col[0]],
            )
            if self.abandoned_col_name:
                _food.is_abandoned = not pd.isna(food[self.abandoned_col[0]])
            if self.inventory_col_name:
                _food.is_inventory = not pd.isna(food[self.inventory_col[0]])
            _foods.append(_food)

        foods = _foods
        foods = sorted(foods, key=lambda f: f.xdate)
        self.bill.foods = foods
        self.spreadsheet.preconsuming.pre_consume_foods()

        return foods
        pass


# The end.
