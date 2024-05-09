import os
import sys

from fnschool import *
from fnschool.canteen.path import *


class Operator:
    def __init__(self, bill):
        self.bill = bill
        self._name = None
        self._dpath = None
        self._preconsuming_dpath = None
        pass

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
        return self._name

    @property
    def dpath(self):
        if not self._dpath:
            self._dpath = user_config_dir / self.name
            if not self._dpath.exists():
                os.makedirs(self._dpath, exist_ok=True)
        return self._dpath

    @property
    def preconsuming_dpath(self):
        if not self._preconsuming_dpath:
            dpath = self.dpath / "preconsuming"
            if not dpath.exists():
                os.makedirs(dpath, exist_ok=True)
            make_link(dpath, canteen_links_dpath / "preconsuming")
            self._preconsuming_dpath = dpath
        return self._preconsuming_dpath
