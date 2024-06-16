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
    def disable_infinite_decimal(self):
        info = _(
            "A story about the infinite decimal:"
            + "\nIn the process of handling bills "
            + "by authors and many bill operators"
            + ", infinite decimals and the "
            + "rounding display of spreadsheet "
            + "have always been the biggest "
            + "trouble. So, We can eliminate it "
            + "through a simple mean. Firstly, "
            + "we take the unit price with "
            + "significant digits and multiply "
            + "it by the quantity to obtain a "
            + "number less than the total "
            + "price. Subtract this number "
            + "from the total price. Then, "
            + "we obtain their difference and "
            + "allocate this difference to some "
            + "unit prices. Finally, we "
            + 'eliminated it in "consuming" '
            + "sheet. "
            + "\nAlthough we have "
            + "made some efforts, we are "
            + "still unable to solve "
            + "some difficult problems "
            + '("Remainder total prices" of '
            + '"food" sheets, etc).'
            + "\n[Ok! I know that, disable the "
            + "infinite decimals for me? (Yes:'Y','y') ]"
        )
        disable_infinite_decimal = self.get_profile(
            key=_("disable infinite decimals"), info=info, allow_blank=True
        )

        return (
            disable_infinite_decimal in "Yy"
            and len(disable_infinite_decimal) > 0
        )

    @property
    def bill_dpath(self):
        dpath = self.dpath / _("bill")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def bill_fpath(self):
        fpath = self.bill_dpath / (_("bill") + ".xlsx")
        if not fpath.exists():
            shutil.copy(bill0_fpath, fpath)
        return fpath

    @property
    def bill_fpath_uuid(self):
        fpath = self.bill_fpath.parent / (
            _("bill") + "." + str(uuid.uuid4()) + ".xlsx"
        )
        return fpath


# The end.
