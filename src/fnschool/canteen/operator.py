import os
import sys
import uuid
import tomllib

from fnschool import *
from fnschool.canteen.path import *


class Operator:
    def __init__(self, bill):
        self.bill = bill
        self._name = None
        self._dpath = None
        self._profile = {}
        self.dpath_showed = False
        pass

    def __str__(self):
        return self.name

    @property
    def name(self):
        if not self._name:
            with open(operator_name_fpath, "r", encoding="utf-8") as f:
                self._name = f.read()
            if self._name == "":
                print_info(_("Tell me your name please:"))
                self._name = input(">_ ")
                with open(operator_name_fpath, "w", encoding="utf-8") as f:
                    f.write(self._name)
                print_info(
                    _('Your name has been saved to "{0}".').format(
                        operator_name_fpath
                    )
                )
            else:
                print_info(
                    _(
                        "Hi, your name is \"{0}\"? (Yes: 'Y' 'y' '', or enter your name)"
                    ).format(self._name)
                )
                n_input = input(">_ ").replace(" ", "")
                if len(n_input) > 1:
                    with open(operator_name_fpath, "w", encoding="utf-8") as f:
                        f.write(n_input)
                    print_info(
                        _('Ok, your name has been saved to "{0}".').format(
                            operator_name_fpath
                        )
                    )
                    self._name = n_input

        return self._name

    @property
    def dpath(self):
        if not self._dpath:
            dpath0 = user_config_dir / self.name
            dpath1 = user_data_dir / self.name
            self._dpath = dpath1
            if not self._dpath.exists():
                os.makedirs(self._dpath, exist_ok=True)
        if not self.dpath_showed:
            print_info(
                _(
                    "Hey! {0}, all of your files will be" 
                    +" saved to {1}, show it now? (Yes: 'Y','y')"
                ).format(
                    self.name,
                    self._dpath
                )
            )
            o_input = input(">_").replace(' ','')
            if len(o_input) > 0 and o_input in 'Yy':
                open_path(self._dpath)
            self.dpath_showed = True
        return self._dpath

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
        fpath = self.config_dpath / (_("food_classes")+".toml")
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
            + "{0} will use it as the form title."
        ).format(app_name)
        superior_department0 = self.get_profile(
            key=_("superior department"), info=info
        )
        return superior_department0

    def get_profile(self, key, info=None):
        profile = self.profile
        if not key in profile.keys():
            print_warning(
                info or _("Please tell {0} the {1}.").format(app_name, key)
            )
            superior_department = None
            for __ in range(0, 3):
                i_value = input(">_").replace(" ", "")
                if len(i_value) > 0:
                    break
                print_error(_("Unexpected value got."))

            self.profile[key] = i_value
            self.save_profile()
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
