import os
import sys
import uuid

from fnschool import *
from fnschool.canteen.path import *


class Operator:
    def __init__(self, bill):
        self.bill = bill
        self._name = None
        self._dpath = None
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
            self._dpath = user_config_dir / self.name
            if not self._dpath.exists():
                os.makedirs(self._dpath, exist_ok=True)
        make_link(self._dpath, self.link_dpath)
        return self._dpath

    @property
    def preconsuming_dpath(self):
        dpath = self.dpath / _("preconsuming")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def link_dpath(self):
        dpath0 = canteen_links_dpath / self.name
        dpath1 = user_documents_dpath / app_name / self.name
        dpath = dpath0
        return dpath

    @property
    def config_dpath(self):
        dpath = self.dpath / _("config")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def food_classes_fpath(self):
        fpath = self.config_dpath / "food_classes.toml"
        if not fpath.exists():
            shutil.copy(food_classes_config0_fpath, fpath)
        return fpath

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
