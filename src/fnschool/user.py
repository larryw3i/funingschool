import os
import sys

from fnschool import *
from fnschool.config import *


class User(ABC):
    def __init__(self, cls):
        self.cls = cls
        self.app = self.cls.app
        self._parent_dpath = None
        self._cfg_fpath = None
        self._cfg = None
        self._name = None
        self._dpath_showed = False
        self._dpath = None
        self._cfg = None
        self._cls_cfg = None
        self._saved_names = None
        self._department_name = None
        self._org_name = None
        self._info_key = _("User Info")
        self.get()

    def get(self):
        user_window = tk.Tk()
        user_window.title(_("User Information"))

        screen_width = user_window.winfo_screenwidth()
        screen_height = user_window.winfo_screenheight()

        window_width = int(screen_width / 4)
        window_height = int(screen_height / 4)

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        user_window.geometry(
            f"{window_width}x{window_height}+{x_position}+{y_position}"
        )

        main_frame = tk.Frame(user_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        name_label = tk.Label(main_frame, text=_("Name:"), anchor="e")
        name_label.grid(row=0, column=0, sticky="e", padx=(0, 5), pady=5)

        name_var = tk.StringVar()
        name_combobox = ttk.Combobox(main_frame, textvariable=name_var)
        name_combobox.grid(row=0, column=1, sticky="ew", padx=(0, 0), pady=5)

        org_label = tk.Label(main_frame, text=_("Organization:"), anchor="e")
        org_label.grid(row=1, column=0, sticky="e", padx=(0, 5), pady=5)

        org_var = tk.StringVar()
        org_entry = tk.Entry(main_frame, textvariable=org_var)
        org_entry.grid(row=1, column=1, sticky="ew", padx=(0, 0), pady=5)

        department_label = tk.Label(
            main_frame, text=_("Department:"), anchor="e"
        )
        department_label.grid(row=2, column=0, sticky="e", padx=(0, 5), pady=5)

        department_var = tk.StringVar()
        department_entry = tk.Entry(main_frame, textvariable=department_var)
        department_entry.grid(row=2, column=1, sticky="ew", padx=(0, 0), pady=5)

        main_frame.grid_columnconfigure(1, weight=1)

        bottom_frame = tk.Frame(user_window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        info_list = self.cls_cfg.get(self._info_key)

        def user_window_destroy():
            self._name = name_var.get() or ""
            self._org_name = org_var.get() or ""
            self._department_name = department_var.get() or ""
            info_list_cp = [[self._name, self._org_name, self._department_name]]
            print(info_list_cp)
            nonlocal info_list
            if info_list:
                for i in info_list:
                    if i[0] and not i[0] == info_list_cp[0][0]:
                        info_list_cp.append(i)

            info_list = info_list_cp
            self.cls_cfg.set(self._info_key, info_list)
            self.cls_cfg.save()

            user_window.destroy()
            pass

        def on_name_var_change(*args):
            info_list0 = [i for i in info_list if i[0] == name_var.get()]
            if not info_list0:
                return
            name, org_name, department_name = info_list0[0]
            if name:
                org_var.set(org_name)
                department_var.set(department_name)
            pass

        name_var.trace("w", on_name_var_change)

        confirm_button = tk.Button(
            bottom_frame, text=_("OK"), command=user_window_destroy
        )
        confirm_button.pack()

        if info_list:
            names = [n[0] for n in info_list]
            name, org_name, department_name = info_list[0]
            name_combobox["values"] = names
            name_var.set(name)
            name_combobox.current(0)
            org_var.set(org_name)
            department_var.set(department_name)

        user_window.mainloop()

        pass

    @property
    def org_name(self):
        return self._org_name

    def __str__(self):
        return self.name

    @property
    def app_cfg(self):
        cfg = self.app.cfg
        return cfg
        pass

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

    @property
    def department_name(self):
        return self._department_name

    @property
    def name(self):
        return self._name
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
