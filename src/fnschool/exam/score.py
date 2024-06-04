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
        self._subject = None
        self._name0 = None
        self._test_t0 = None
        self._test_t1 = None
        self._fpath = None
        self._fpaths = None
        self._scores = None
        self.fext = ".xlsx"

        pass

    @property
    def teacher(self):
        if not self._teacher:
            self._teacher = Teacher()
        return self._teacher

    def enter(self):
        pass

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

        self._fpaths = sorted(self._fpaths, key=lambda f: f[-1])

        return self._fpaths

    @property
    def scores(self):
        if not self._scores:
            self.read_scores()
        return self._scores

    @property
    def grade(self):
        if not self._grade:
            self.read_scores()
        return self._grade

    @property
    def subject(self):
        if not self._subject:
            self.read_scores()
        return self._subject

    @property
    def test_t0(self):
        if not self._test_t0:
            self.read_scores()
        return self._test_t0

    @property
    def test_t1(self):
        if not self._test_t1:
            self.read_scores()
        return self._test_t1

    @property
    def name0(self):
        if not self._name0:
            self.read_scores()
        return self._name0

    def read_scores(self):

        if self._scores:
            return

        fpath = self.fpath
        fpaths = self.fpaths
        fpath1 = None if len(fpaths) < 2 else fpaths[1]

        scores1 = None
        scores1_name = None
        if fpath1:
            wb = load_workbook(fpath1)
            sheet = wb.active
            scores1_name = sheet.cell(1, 1).value().split("\n")[2]
            scores1 = [
                [sheet.cell(row_index, 1).value, sheet.cell(row_index, 2).value]
                for row_index in range(2, sheet.max_row + 1)
            ]
            scores1 = [
                [n, s]
                for n, s in scores1
                if ((not "平均分" in n) and len(n.strip()) > 0)
            ]
            wb.close()
            sheet = None

        wb = load_workbook(fpath)
        sheet = wb.active

        sheet.cell(1, 3, scores1_name if scores1_name else _("No recent tests"))
        for row_index in range(2, sheet.max_row + 1):
            name = sheet.cell(row_index, 1).value
            if name:
                score = [s for n, s in scores1 if n == name] if scores1 else []
                score = score[0] if len(score) > 0 else 0
                sheet.cell(row_index, 3, score)

        print_info(
            _(
                "The recent examination scores " + 'have been added to "{0}".'
            ).format(fpath)
            if scores1
            else _("There is no recent tests.")
        )
        wb.save(fpath)
        print_info(_('Spreadsheet "{0}" has been saved.').format(fpath))
        wb.close()
        sheet = None

        print_info(
            _(
                "Please update the question titles "
                + "and scores "
                + 'of "{0}" '
                + "according to the comments. "
                + "(Ok, open it for me [Press any "
                + "key to open file])"
            ).format(fpath)
        )
        input(">_ ")
        open_path(fpath)
        print_warning(
            _(
                "Ok, I have updated the question"
                + " titles and scores, and I closed "
                + "the file. "
                + "(Press any key to continue)"
            )
        )
        input(">_ ")

        scores = pd.read_excel(fpath)
        scores_col_0 = scores.columns[0].split("\n")
        self._grade = scores_col_0[0]
        self._subject = scores_col_0[1]
        self._name0 = scores_col_0[2]

        if len(scores_col_0) > 3:
            self._test_t0 = datetime.strptime(scores_col_0[3], "%Y%m%d%H%M")
            self._test_t1 = datetime.strptime(scores_col_0[4], "%Y%m%d%H%M")

        scores.rename(columns={scores.columns[0]: "姓名"}, inplace=True)
        scores.drop(scores.tail(1).index, inplace=True)

        self._scores = scores

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

                names_len2 = len(str(names_len))
                print_warning(
                    sqr_slist(
                        [f"{i:>{names_len2}} {n}" for i, n in enumerate(names)]
                    )
                )
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
