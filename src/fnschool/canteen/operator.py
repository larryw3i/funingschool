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
        self._name = None
        self._dpath = None
        self._profile = {}
        self._config = None
        pass

    @property
    def config(self):
        if not self._config:
            self._config = Config(
                (self.config_dpath / (_("app_config") + ".toml"))
            )

        return self._config

    @property
    def preconsuming_dpath(self):
        dpath = self.dpath / _("preconsuming")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def config_dpath(self):
        dpath = self.dpath / _("config")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def food_classes_fpath(self):
        fpath = self.config_dpath / (_("food_classes") + ".toml")
        if not fpath.exists():
            shutil.copy(food_classes_config0_fpath, fpath)
        return fpath

    def save_profile(self):
        profile = self.profile
        with open(self.profile_fpath, "w", encoding="utf-8") as f:
            f.write("\n".join([f'"{k}"="{v}"\n' for k, v in profile.items()]))
        return profile

    @property
    def profile_fpath(self):
        fpath = self.config_dpath / (_("profile") + ".toml")
        if not fpath.exists():
            with open(fpath, "w+", encoding="utf-8") as f:
                f.write("")
        return fpath

    @property
    def profile(self):
        if not self._profile:
            with open(self.profile_fpath, "rb") as f:
                self._profile = tomllib.load(f)
        return self._profile

    @property
    def superior_department(self):
        info = _(
            "Please tell {0} your superior department, "
            + "{0} will use it as the form title. "
            + '("purchasing summary" form, '
            + '"consuming summary" form, etc.)'
        ).format(app_name)
        superior_department0 = self.get_profile(
            key=_("superior department"), info=info
        )
        return superior_department0

    def get_profile(self, key, info=None):
        profile = self.profile
        if not key in profile.keys() or profile.get(key).strip() == "":
            print_warning(
                info or _("Please tell {0} the {1}.").format(app_name, key)
            )
            for i in range(0, 3):
                i_value = input(">_ ").replace(" ", "")
                if len(i_value) > 0:
                    break
                print_error(_("Unexpected value got."))
                if i >= 2:
                    exit()

            self.profile[key] = i_value
            self.save_profile()
            print_info(
                _(
                    '"{0}" has been saved to "{1}". '
                    + "(Ok! I know that. "
                    + "[Press any key to continue])"
                ).format(key, self.profile_fpath)
            )
            input(">_ ")

        return self.profile[key]

    @property
    def bill_dpath(self):
        dpath = self.dpath / _("bill")
        if not dpath.exists():
            os.makedirs(dpath)
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
