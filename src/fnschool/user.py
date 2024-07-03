import os
import sys

from fnschool import *
from fnschool.config import *


class User:
    def __init__(self, parent_dpath=None, name_fpath=None, ask_name_s=None):
        self.parent_dpath = parent_dpath
        self.name_fpath = name_fpath
        self.ask_name_s = ask_name_s or _("Enter your name, please!")

        self._name = None
        self.dpath_showed = False
        self._dpath = None
        self._profile = {}
        self._config = None
        self.is_male_key = _("is_male")

    def __str__(self):
        return self.name

    def save_profile(self):
        profile = self.profile
        with open(self.profile_fpath, "w", encoding="utf-8") as f:
            f.write("\n".join([f'"{k}"="{v}"' for k, v in profile.items()]))
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

    def get_profile(self, key, info=None, allow_blank=False):
        profile = self.profile
        if not key in profile.keys() or profile.get(key).strip() == "":
            print_warning(
                info or _("Please tell {0} the {1}.").format(app_name, key)
            )
            i_value = None
            for i in range(0, 3):
                i_value = input0().replace(" ", "")
                if len(i_value) > 0:
                    break
                if allow_blank:
                    i_value = ""
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
            input0()

        return self.profile[key]

    @property
    def is_male(self):
        m = self.get_profile(
            self.is_male_key,
            info=_(
                "Excuse me, could you tell me your gender? "
                + "('F' for \"Female\", 'M' for \"Male\","
                + "default: 'F')"
            ),
        )
        return m.lower() == "m"

    @property
    def name(self):
        name_writed_s = _('Your name has been saved to "{0}".').format(
            self.name_fpath
        )

        if not self._name:
            name = None
            with open(self.name_fpath, "r", encoding="utf-8") as f:
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
                ).format(self.name_fpath)
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

                    n_input = input0()

                    if n_input.isnumeric():
                        n_input = int(n_input) - 1
                        if n_input > names_len or n_input < 0:
                            continue
                        name0 = names[n_input]
                        if name0.startswith(">"):
                            name0 = name0[1:]
                        break

                    elif n_input == "":
                        self._name = name0
                        break
                    else:
                        name0 = n_input
                        break

                if not self._name:
                    if name0 in names:
                        names.remove(name0)
                    elif (">" + name0) in names:
                        names.remove((">" + name0))

                    self._name = name0
                    name0 = ">" + name0
                    names = [n.replace(">", "") for n in names]

                    with open(self.name_fpath, "w", encoding="utf-8") as f:
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

                    with open(self.name_fpath, "w", encoding="utf-8") as f:
                        f.write("\n".join([name0, name]))

                    print_info(name_writed_s)
                    self._name = n_input
                else:
                    self._name = name

            else:

                print_warning(self.ask_name_s)
                for i in range(0, 3):
                    n_input = input0().replace(" ", "")
                    n_input_len = len(n_input)
                    if n_input_len > 0:
                        self._name = n_input
                        break
                    elif n_input_len < 1 and i < 3:
                        print_error(_("Unexpected value was got."))
                    else:
                        print_error(_("Unexpected value was got. Exit."))
                        exit()

                with open(self.name_fpath, "w", encoding="utf-8") as f:
                    f.write(">" + self._name)

                print_info(name_writed_s)

        return self._name

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
            o_input = input0().replace(" ", "")
            if len(o_input) > 0 and o_input in "Yy":
                open_path(self._dpath)
            self.dpath_showed = True
        return self._dpath

    @property
    def config(self):
        if not self._config:
            self._config = Config(
                (self.config_dpath / (_("app_config") + ".toml"))
            )

        return self._config

    @property
    def config_dpath(self):
        dpath = self.dpath / _("config")
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath


# The end.
