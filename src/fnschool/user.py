import os
import sys

from fnschool import *
from fnschool.config import *


class User:
    def __init__(self, config_fpath, parent_dpath=None, ask_name_s=None):
        self.config_fpath = config_fpath
        self.parent_dpath = parent_dpath or self.config_fpath.parent
        self.ask_name_s = ask_name_s or _("Enter your name, please!")

        self._name = None
        self.dpath_showed = False
        self._dpath = None
        self._profile = {}
        self._config = None
        self.is_male_key = _("is_male")
        self._saved_names = None
        self.use_tk = use_tk()
        self.saved_names_key = _("Saved Name")

    def __str__(self):
        return self.name

    @property
    def saved_names(self):
        if not self._saved_names:
            names = self.config.get(self.saved_names_key, [""])
            self._saved_names = names
        return self._saved_names
        pass

    def save_name(self, name):
        if len(name.strip()) > 0:
            self._saved_names = [
                n for n in self._saved_names if len(n.strip()) > 0
            ]

            if name in self._saved_names:
                if self._saved_names[0] == name:
                    return
                else:
                    self._saved_names.remove(name)
                    pass

            self._saved_names.insert(0, name)
            self.config[self.saved_names_key] = self._saved_names
            self.save_config()
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
        name_writed_s = _('Your name has been saved to "{0}".').format(
            self.config_fpath
        )

        name = None
        name1 = None
        with open(self.config_fpath, "r", encoding="utf-8") as f:
            name = f.read().replace(" ", "").strip()

        print_info(
            (
                _('The saved names have been read from "{0}".')
                if "\n" in name
                else (
                    _('No name was read from "{0}".')
                    if len(name) < 1
                    else _('The saved name has been read from "{0}".')
                )
            ).format(self.config_fpath)
        )

        if "\n" in name:
            names = name.split("\n")

            name0 = None
            if ">" in name:
                name0 = name.split(">")[1]
                if "\n" in name0:
                    name0 = name0.split("\n")[0]
            else:
                name0 = names[0]

            print_info(
                _("The names saved by {0} are as follows:").format(app_name)
            )

            names_len = len(names)
            names_len2 = len(str(names_len))
            name_s = sqr_slist(
                [f"({i+1:>{names_len2}}) {n}" for i, n in enumerate(names)]
            )
            print_warning(name_s)

            for i in range(0, 3):
                if i > 2:
                    print_error(_("Unexpected value was got. Exit."))
                    exit()

                print_info(
                    _(
                        "Enter the Number of your name, "
                        + 'or enter your name. ("Enter" for "{0}")'
                    ).format(name0)
                )

                n_input = get_input()

                if n_input.isnumeric():
                    n_input = int(n_input) - 1
                    if n_input > names_len or n_input < 0:
                        continue
                    name0 = names[n_input]
                    if name0.startswith(">"):
                        name0 = name0[1:]
                    break

                elif n_input == "":
                    name1 = name0
                    break
                else:
                    name0 = n_input
                    break

            if not name1:
                if name0 in names:
                    names.remove(name0)
                elif (">" + name0) in names:
                    names.remove((">" + name0))

                name1 = name0
                name0 = ">" + name0
                names = [n.replace(">", "") for n in names]

                with open(self.config_fpath, "w", encoding="utf-8") as f:
                    f.write("\n".join([name0] + names))

                print_info(name_writed_s)

        elif len(name) > 0:

            if ">" in name:
                name = name[1:]

            print_warning(
                _(
                    "Hi~ is {0} your name? or enter your "
                    + "name, please! (Yes: 'Y','y','')"
                ).format(name)
            )

            n_input = input("> ").replace(" ", "")
            if not n_input in "Yy":
                name0 = ">" + n_input

                with open(self.config_fpath, "w", encoding="utf-8") as f:
                    f.write("\n".join([name0, name]))

                print_info(name_writed_s)
                name1 = n_input
            else:
                name1 = name

        else:

            print_warning(self.ask_name_s)
            for i in range(0, 3):
                n_input = get_input().replace(" ", "")
                n_input_len = len(n_input)
                if n_input_len > 0:
                    name1 = n_input
                    break
                elif n_input_len < 1 and i < 3:
                    print_error(_("Unexpected value was got."))
                else:
                    print_error(_("Unexpected value was got. Exit."))
                    exit()

            with open(self.config_fpath, "w", encoding="utf-8") as f:
                f.write(">" + name1)

            print_info(name_writed_s)

        return name1

    @property
    def dpath(self):
        if not self._dpath:
            dpath = self.parent_dpath / self.name
            self._dpath = dpath
            if not self._dpath.exists():
                os.makedirs(self._dpath, exist_ok=True)

        if not self.dpath_showed:
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
            self.dpath_showed = True
        return self._dpath

    @property
    def config(self):
        if not self._config:
            with open(self.config_fpath, "r", encoding="utf-8") as f:
                self._config = tomlkit.load(f)

        return self._config

    def save_config(self):
        with open(self.config_fpath, "w", encoding="utf-8") as f:
            tomlkit.dump(self.config, f)

        pass


# The end.
