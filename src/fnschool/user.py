import os
import sys

from fnschool import *


class User:
    def __init__(
        self,
        parent_dpath=None,
        name_fpath=None,
    ):
        self.parent_dpath = parent_dpath
        self.name_fpath = name_fpath

        self._name = None
        self.dpath_showed = False

    def __str__(self):
        return self.name

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

                    n_input = input(">_ ")

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

                print_warning(_("Enter your name, please!"))
                for i in range(0, 3):
                    n_input = input(">_ ").replace(" ", "")
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
            o_input = input(">_ ").replace(" ", "")
            if len(o_input) > 0 and o_input in "Yy":
                open_path(self._dpath)
            self.dpath_showed = True
        return self._dpath


# The end.
