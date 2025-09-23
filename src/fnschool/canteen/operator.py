import os
import sys
import uuid
import tomllib

from fnschool import *
from fnschool.canteen.path import *
from fnschool.canteen.config import *


class Operator(User):
    def __init__(self, bill):
        super().__init__(bill)
        self.bill = bill
        self.workbook_ext = ".xlsx"
        pass

    @property
    def preconsuming_dpath(self):
        dpath = self.dpath / _("preconsuming")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def food_classes_fpath(self):
        fpath = self.dpath / (_("food_classes") + ".toml")
        if not fpath.exists():
            shutil.copy(food_classes_config0_fpath, fpath)
        return fpath

    @property
    def superior_department(self):
        superior_department = self.department_name
        return superior_department0

    @property
    def bill_dpath(self):
        dpath = self.dpath / _("bill")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def bill_fpath(self):
        fpath = self.get_bill_fpath()
        return fpath

    def get_bill_fpath(self, mtype=None):
        fpath = self.bill_dpath / (
            _("bill")
            + (
                (
                    _("({0})").format(self.bill.meal_type)
                    if self.bill.meal_type
                    else ""
                )
                if not mtype
                else _("({0})").format(mtype)
            )
            + self.workbook_ext
        )
        if not fpath.exists():
            shutil.copy(bill0_fpath, fpath)
        return fpath

    @property
    def bill_fpath_uuid(self):
        fpath = (
            str(self.bill_fpath).rpartition(".")[0]
            + "."
            + str(uuid.uuid4())
            + self.bill_fpath.suffix
        )
        return fpath


# The end.
