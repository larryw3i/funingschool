import os
import sys
import time
from fnschool import *
from fnschool.exam import *
from fnschool.exam.path import *
from fnschool.exam.teacher import *


class Score:
    def __init__(
        self,
    ):
        self._name = None
        self._teacher = None
        self.fpath0 = score_fpath0
        self._grade = None
        self._fpath = None
        self._fpaths = None
        self.fext = ".xlsx"
        pass

    @property
    def teacher(self):
        if not self._teacher:
            self._teacher = Teacher()
        return self._teacher

    def enter(self):
        # self.update_questions()
        print(self.fpaths)

    @property
    def fpaths(self):
        if not self._fpaths:
            dpath = self.fpath.parent.as_posix()
            fpaths = []
            for f in os.listdir(dpath):
                if f.endswith(self.fext):
                    fpath = Path(dpath) / f
                    wb = load_workbook(fpath)
                    sheet = wb.active
                    test_time = (
                        sheet.cell(1, 1).value.split("\n")
                        if sheet.cell(1, 1).value
                        else []
                    )
                    if len(test_time) > 3:
                        fpaths.append(
                            [
                                fpath,
                                datetime.strptime(test_time[3], "%Y%m%d%H%M"),
                                datetime.strptime(test_time[4], "%Y%m%d%H%M"),
                            ]
                        )

                    else:
                        wb.close()
                        sheet = None
                        test_time = datetime.fromtimestamp(
                            os.path.getctime(fpath)
                        )
                        fpaths.append([fpath, test_time])
            self._fpaths = fpaths
        return self._fpaths

    def update_questions(self):
        fpath = self.fpath
        print_info(
            _(
                "Please update the question titles "
                + 'of "{0}" '
                + "according to the comments. "
                + "(Ok, open it for me [Press any "
                + "key to open file])"
            ).format(fpath)
        )
        input(">_ ")
        open_path(fpath)
        print_warning(_("Ok, I have updated it. (Press any key to continue)"))
        input(">_ ")
        return

    @property
    def name_fpath(self):
        fpath = self.teacher.dpath / (_("exam_names") + ".txt")
        if not fpath.exists():
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("")
        return fpath

    @property
    def fpath(self):
        if not self._fpath:
            self._fpath = self.teacher.exam_dpath / (
                Path(self.name).as_posix() + self.fext
            )
            if not self._fpath.parent.exists():
                os.makedirs(self._fpath.parent.as_posix(), exist_ok=True)
            if not self._fpath.exists():
                shutil.copy(self.fpath0, self._fpath)

        return self._fpath

    @property
    def name(self):
        if not self._name:
            names = None
            with open(self.name_fpath, "r", encoding="utf-8") as f:
                names = f.read().replace(" ", "").strip().split("\n")
            names = [n for n in names if (len(n) > 0)]
            names_len = len(names)

            name_writed_s = _(
                "The name of examination " + 'has been saved to "{0}".'
            ).format(self.name_fpath)

            if names_len > 0:
                name0 = (
                    names[0]
                    if not any([n.startswith(">") for n in names])
                    else [n for n in names if n.startswith(">")][0].replace(
                        ">", ""
                    )
                )
                print_error(
                    (
                        _("The saved examination names are as follow:")
                        if names_len > 1
                        else _("The saved examination name is as follow:")
                    )
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
                    n_input = input(">_ ").replace(" ", "")
                    if len(n_input) > 0:
                        if n_input.isnumeric():
                            n_input = int(n_input) - 1
                            if n_input >= 0 and n_input <= names_len:
                                name_i = names[n_input]
                                break
                            break
                        else:
                            name_i = n_input
                            break
                    else:
                        name_i = name0
                        break

                    if i > 2:
                        print_error(_("Unexpected value was got. Exit."))
                        exit()
                    else:
                        print_error(_("Unexpected value was got."))

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
                    _(
                        "Hello~ tell {0} the examination" + " name, please!"
                    ).format(app_name)
                )
                for i in range(0, 3):
                    name0 = input(">_ ").replace(" ", "")
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

        if self._name.startswith("/"):
            self._name = re.sub(r"^/+", "", self._name)
        if self._name.startswith("\\"):
            self._name = re.sub(r"^\\+", "", self._name)
        if ".." in self._name:
            self._name = re.sub("..", "", self._name)

        if "/" in self._name:
            dpath = (self.teacher.exam_dpath / Path(self._name)).parent
            if not dpath.exists():
                os.makedirs(dpath, exist_ok=True)

        return self._name


# The end.
