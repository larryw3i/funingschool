import os
import sys

from fnschool import *
from fnschool.config import *


class User(ABC):
    def __init__(self, cls, ask_name_str=None):
        self.cls = cls
        self.app = self.cls.app
        self.use_tk = self.app.use_tk
        self._parent_dpath = None
        self._cfg_fpath = None
        self._cfg = None
        self.ask_name_str = ask_name_str or _("Enter your name, please!")
        self._name = None
        self._dpath_showed = False
        self._dpath = None
        self._profile = {}
        self._cfg = None
        self._cls_cfg = None
        self.is_male_key = _("Is Male")
        self._saved_names = None
        self.saved_names_key = _("Saved User Names")
        self._department_name = None
        self.saved_department_name_key = _("Department Name")

    def __str__(self):
        return self.name

    @property
    def cfg(self):
        if not self._cfg:
            self._cfg = UserConfig(self)
        return self._cfg

    @property
    def cls_cfg(self):
        if not self._cls_cfg:
            self._cls_cfg = self.cls.cfg
        return self._cls_cfg

    def _get_department_name_from_tk(self):
        tip = _("Enter your department name:")
        title = _("Department name")
        key = self.saved_department_name_key
        department_name = self.cls_cfg.select(title, tip, key)
        return department_name
        pass

    @property
    def department_name(self):
        if not self._department_name:
            self._department_name = (
                self._get_department_name_from_tk()
                if self.use_tk
                else self._get_department_name_from_cli()
            )
        return self._department_name

    def _get_department_name_from_cli(self):
        department_name = None
        if self.use_tk:
            pass
        else:
            print_error(_("The function has not been implemented."))
            pass
        return department_name
        pass

    def _get_name_from_tk(self):
        tip = _("Enter your name:")
        title = self.ask_name_str
        key = self.saved_names_key
        name = self.cls_cfg.select(key, title, tip)
        return name
        pass

    @property
    def name(self):
        if not self._name:
            self._name = (
                self._get_name_from_tk()
                if self.use_tk
                else self._get_name_from_cli()
            )
            pass

        return self._name
        pass

    def _get_name_from_cli(self):
        name = None
        if self.use_tk:
            pass
        else:
            print_error(_("The function has not been implemented."))
            pass
        return name
        pass

    @property
    def dpath(self):
        if not self._dpath:
            dpath = (
                get_share_dpath(Path(inspect.getfile(self.__class__))).parent
                / self.name
            )
            self._dpath = dpath
            if not self._dpath.exists():
                os.makedirs(self._dpath, exist_ok=True)

        if not self._dpath_showed:
            if not self.app.use_tk:
                print_info(
                    _(
                        "Hey! {0}, all of your files will be"
                        + ' saved to "{1}", show it now? '
                        + "(yes: 'y','y')"
                    ).format(self.name, self._dpath)
                )
                o_input = get_input().replace(" ", "")
                if len(o_input) > 0 and o_input in "Yy":
                    open_path(self._dpath)
            else:
                from tkinter import messagebox

                response = messagebox.askyesno(
                    _("Open your directory?"),
                    _(
                        "Hey! {0}, all of your files will be"
                        + ' saved to "{1}", show it now? '
                    ).format(self.name, self._dpath),
                )
                if response:
                    open_path(self._dpath)
                    pass
            self._dpath_showed = True
            pass

        return self._dpath

    @property
    def cfg_fpath(self):
        if not self._cfg_fpath:
            dpath = self.dpath
            if not dpath.exists():
                os.makedirs(dpath, exist_ok=True)
            fpath = dpath / (_("config") + ".toml")

            self._cfg_fpath = fpath
        return self._cfg_fpath

        pass


# The end.
