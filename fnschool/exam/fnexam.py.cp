import os
import sys

from fnschool import *
from fnschool.exam import *
from fnschool.exam.path import *


class FnExam:
    def __init__(
        self,
        teacher,
    ):
        self._name = None
        self.teacher = teacher
        self.fpath0 = score_fpath0
        self._grade = None
        pass

    @property
    def name_fpath(self):
        return self.teacher.dpath / (_("exam_names") + ".txt")

    @property
    def name(self):
        if not self._name:
            names = None
            with open(self.name_fpath, "r", encoding="utf-8") as f:
                names = f.read().replace(" ", "").strip().split("\n")
            names = [n for n in names if (len(n) > 0)]
            name0 = (
                names[0]
                if not any([n.startswith(">") for n in names])
                else [n for n in names if n.startswith(">")][0].replace(">", "")
            )

            names_len = len(names)

            if names_len > 0:
                name_writed_s = _(
                    "The name of examination " + 'has been saved to "{0}".'
                ).format(self.name_fpath)

                print_error(
                    (
                        _("The saved examination names {0} " + "are as follow:")
                        if names_len > 1
                        else _(
                            "The saved examination name {0}" + "is as follow:"
                        )
                    ).format(app_name)
                )

                print_warning(sqr_slist(names))
                names = [n.replace(">", "") for n in names]
                print_info(
                    _(
                        "Select the examination name "
                        + "you entered (index), "
                        + "or enter new examination "
                        + "name, please! (default: {0})"
                    ).format(name0)
                )
                name_i = None
                for i in range(0, 3):
                    n_input = input().replace(" ", "")
                    if len(n_input) > 0:
                        if n_input.is_numeric():
                            n_input = int(n_input) - 1
                            if n_input < 0 or n_input > names_len:
                                print_error(_("Unexpected value was got."))
                            else:
                                name_i = names[n_input]

                                break
                        else:
                            name_i = n_input
                            break

                    if i > 2:
                        print_error(_("Unexpected value was got. Exit."))
                        exit()

                if name_i != name0:
                    if name_i in names:
                        names.remove(name_i)
                    with open(self.name_fpath, "w", encoding="utf-8") as f:
                        f.write("\n".join([">" + name_i] + names))
                    name0 = name_i
                    print_info(name_writed_s)

                self._name = name0

            else:
                print_info(
                    _("Hello~ tell {0} your name, please!").format(app_name)
                )
                for i in range(0, 3):
                    name0 = input().replace(" ", "")
                    if len(name0) > 0:
                        self._name = name0
                        break
                    else:
                        print_error(_("Unexpected value was got."))
                    if i > 2:
                        print_error(_("Unexpected value was got." + " Exit."))
                        exit()
                with open(self.name_fpath, "w", encoding="utf-8") as f:
                    f.write(">" + self._name)
                print_info(name_writed_s)

        return self._name


# The end.
