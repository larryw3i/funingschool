import os
import sys
import uuid
import tomllib

from fnschool import *
from fnschool.canteen.path import *
from fnschool.canteen.config import *


class Operator(User):
    def __init__(self, bill):
        super().__init__(user_canteen_dpath, operator_name_fpath)
        self.bill = bill
        pass

    @property
    def preconsuming_dpath(self):
        dpath = self.dpath / _("preconsuming")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def food_classes_fpath(self):
        fpath = self.config_dpath / (_("food_classes") + ".toml")
        if not fpath.exists():
            shutil.copy(food_classes_config0_fpath, fpath)
        return fpath

    @property
    def superior_department(self):
        info = _(
            "Please tell {0} the alias of your "
            + "superior department, "
            + "{0} will use it as the form title ("
            + '"purchasing summary" form, '
            + '"consuming summary" form, etc). '
            + 'e.g: "富宁县那能乡中小学". '
            + "If you haven't noticed it, "
            + "you can check the previous bill "
            + "first and then let {0} know."
        ).format(app_name)
        superior_department0 = self.get_profile(
            key=_("superior department"), info=info
        )
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
            + ".xlsx"
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
