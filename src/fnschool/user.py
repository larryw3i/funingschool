import os
import sys

from fnschool import *
from fnschool.config import *


class User:
    def __init__(self, cls, ask_name_s=None):
        self.cls = cls
        self._parent_dpath = None
        self._cfg_fpath = None
        self._cfg = None
        self.ask_name_s = ask_name_s or _("Enter your name, please!")
        self._name = None
        self._dpath_showed = False
        self._dpath = None
        self._profile = {}
        self._cfg = None
        self._cls_cfg = None
        self.is_male_key = _("Is Male")
        self._saved_names = None
        self.use_tk = use_tk()
        self.saved_names_key = _("Saved Name")

    def __str__(self):
        return self.name

    @property
    def cfg(self):
        if not self._cfg:
            self._cfg = UserConfig(self.cfg_fpath)
        return self._cfg

    @property
    def cls_cfg(self):
        if not self._cls_cfg:
            self._cls_cfg = self.cls.cfg.cls
        return self._cls_cfg

    @property
    def saved_names(self):
        if not self._saved_names:
            names = self.cls_cfg.data.get(self.saved_names_key, [""])
            self._saved_names = names
        return self._saved_names
        pass

    def save_name(self, name):
        if len(name.strip()) > 0:
            if self._saved_names:
                self._saved_names = [
                    n for n in self._saved_names if len(n.strip()) > 0
                ]

                if name in self._saved_names:
                    if self._saved_names[0] == name:
                        return
                    else:
                        self._saved_names.remove(name)
                        pass
            else:
                self._saved_names = []
            self._saved_names.insert(0, name)
            self.cls_cfg.data[self.saved_names_key] = self._saved_names

            pass

        pass

        if not self.use_tk:
            print_info(_('Name "%s" has been saved.'))

        pass

    @property
    def name(self):
        if not self._name:
            self._name = (
                self.get_name_from_tk()
                if self.use_tk
                else self.get_name_from_cli()
            )
            pass

        return self._name

    def get_name_from_tk(self):
        name = None
        root = tk.Tk()
        root.title(self.ask_name_s)
        root.bind("<Return>", lambda e: root.destroy())

        name_var = tk.StringVar()
        notername_label = tk.Label(root, text=_("Enter your name:"))
        notername_combo = ttk.Combobox(
            root, textvariable=name_var, values=self.saved_names
        )
        notername_combo.set(self.saved_names[0])
        submit_button = tk.Button(
            root,
            text=_("OK"),
        )
        closing_lambda = lambda: [root.destroy()]
        submit_button.config(command=closing_lambda)
        notername_label.grid(row=0, column=0)
        notername_combo.grid(row=0, column=1)
        submit_button.grid(row=1, column=1, sticky=tk.E)
        notername_combo.focus_set()
        root.mainloop()

        name = name_var.get()
        self.save_name(name)
        return name
        pass

    def get_name_from_cli(self):
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
            print_info(
                _(
                    "Hey! {0}, all of your files will be"
                    + ' saved to "{1}", show it now? '
                    + "(Yes: 'Y','y')"
                ).format(self.name, self._dpath)
            )
            o_input = get_input().replace(" ", "")
            if len(o_input) > 0 and o_input in "Yy":
                open_path(self._dpath)
            self._dpath_showed = True
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
