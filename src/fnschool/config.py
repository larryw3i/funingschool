import os
import sys

from abc import ABC
from fnschool import *


class ConfigBase(ABC):
    def __init__(self, parent):
        self.parent = parent
        self._cfg_fpath = self.parent.cfg_fpath
        self.use_tk = (
            self.parent.use_tk if hasattr(self.parent, "use_tk") else False
        )
        self._data = {}

        pass

    @property
    def path(self):
        if not self._cfg_fpath.exists():
            os.makedirs(self._cfg_fpath.parent, exist_ok=True)
            with open(self._cfg_fpath, "w", encoding="utf-8") as f:
                f.write("")
                pass

        return self._cfg_fpath

    @property
    def data(self):
        if self._data == {}:
            with open(self.path, "rb") as f:
                self._data = tomlkit.load(f)
                if not self._data:
                    self._data = {}
            print_info(
                _("Configurations has been " + 'read from "{0}".').format(
                    self.path
                )
            )
        return self._data
        pass

    def save(self):
        data = self.data
        with open(self.path, "w", encoding="utf-8") as f:
            tomlkit.dump(data, f)
            pass
        print_info(_("Configuration data has been saved!"))
        pass

    def get(self, key):
        value = self.data.get(key)
        return value
        pass

    def set(self, key, value):
        self.data[key] = value
        pass

    def select(self, key, title=None, tip=None):
        name = None
        root = tk.Tk()
        root.title(title)
        root.bind("<Return>", lambda e: root.destroy())

        title = title or _("Select or entry a value")
        tip = tip or _("Value:")
        key = key
        values = self.get(key) or [""]

        value_var = tk.StringVar()
        value_label = tk.Label(root, text=tip)
        value_combo = ttk.Combobox(root, textvariable=value_var, values=values)
        value_combo.set(values[0])
        submit_button = tk.Button(
            root,
            text=_("OK"),
        )
        closing_lambda = lambda: [root.destroy()]
        submit_button.config(command=closing_lambda)
        value_label.grid(row=0, column=0)
        value_combo.grid(row=0, column=1)
        submit_button.grid(row=1, column=1, sticky=tk.E)
        value_combo.focus_set()
        root.mainloop()

        value = value_var.get()

        if len(value.strip()) > 0:
            if values:
                values = [n for n in values if len(n.strip()) > 0]

                if value in values:
                    if values[0] == value:
                        return value
                    else:
                        values.remove(value)
                        pass
            else:
                values = []
            values.insert(0, value)
            self.set(key, values)
            pass

        if not self.use_tk:
            print_info(_('Name "%s" has been saved.'))

        return value
        pass


class ClsConfig(ConfigBase):
    def __init__(self, parent):
        ConfigBase.__init__(self, parent)
        pass


class UserConfig(ConfigBase):
    def __init__(self, parent):
        ConfigBase.__init__(self, parent)


class AppConfig(ConfigBase):
    def __init__(self, parent):
        ConfigBase.__init__(self, parent)

        pass

    pass


# The end.
