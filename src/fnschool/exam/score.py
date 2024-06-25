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
        self._full_name = None
        self._teacher = None
        self.fpath0 = score_fpath0
        self._grade = None
        self._subject = None
        self._short_name = None
        self._short_name_m2 = None
        self._test_t = None
        self._fpath = None
        self._dpath = None
        self._fpath_m2 = None
        self._fpaths = None
        self._scores_m1 = None
        self._wb = None
        self._total_points = None
        self._sheet0 = None
        self._scores = None
        self.p_path_key = _("scores_parent_directory")
        self._question_titles = None
        self.fext = ".xlsx"
        self.no_test_m2_s = _("No recent tests")
        self.name_index0 = 3
        self.question_index0 = 4
        self.points_index0 = self.question_index0 - 1

        pass

    @property
    def dpath(self):
        if not self._dpath:
            self._dpath = self.fpath.parent
        return self._dpath

    @property
    def config(self):
        return self.teacher.config

    @property
    def teacher(self):
        if not self._teacher:
            self._teacher = Teacher()
        return self._teacher

    def enter(self):
        scores = self.scores
        print(scores)
        pass

    def read(self):

        p_dpath = self.config.get(self.p_path_key)
        if p_dpath == ".":
            p_dpath = None
        initialdir = (
            p_dpath
            if (p_dpath and Path(p_dpath).exists())
            else self.teacher.exam_dpath
        )

        filetypes = ((_("Spreadsheet Files"), "*.xlsx"),)

        tkroot = tk.Tk()
        tkroot.withdraw()

        filename = filedialog.askopenfilename(
            title=_("Please select the scores file"),
            initialdir=initialdir,
            filetypes=filetypes,
        )

        if (
            filename is None
            or filename == ()
            or filename == "."
            or filename == ""
        ):
            print_warning(_("No file was selected, exit."))
            exit()

        print_info(_('Scores file "{0}" has been selected.').format(filename))
        self.config.save(self.p_path_key, Path(filename).parent.as_posix())
        self.name = filename
        print(self.scores)
        print(self.scores)

    def get_scores(self, fpath):
        if not Path(fpath).exists():
            return None

        scores = pd.read_excel(fpath, skiprows=[0, 2])
        scores.rename(columns={scores.columns[0]: "姓名"}, inplace=True)
        scores.set_index("姓名", inplace=True)
        scores["考试纪律"] = scores["考试纪律"].fillna(0)
        point_cols = scores.columns[self.points_index0 :].to_list()
        scores["总分"] = scores.loc[:, point_cols].sum(axis=1)
        scores.drop([scores.columns[2]], axis=1, inplace=True)

        return scores

    @property
    def scores(self):
        if self._scores is None:
            fpaths = self.fpaths

            if len(fpaths) < 1:
                return None

            fpaths = fpaths[::-1]
            scores_cols = ["Name"]
            scores_rows = None

            for fi, (f, __) in enumerate(fpaths):
                name = Path(f).stem
                scores_cols.append(name)
                f_scores = self.get_scores(f)
                s_index = f_scores.index.to_list()
                if not scores_rows:
                    scores_rows = [[n] for n in s_index]

                for i in range(len(scores_rows)):
                    r = scores_rows[i]
                    s_name = r[0]

                    if s_name in s_index:
                        r.append(f_scores.loc[s_name, f_scores.columns[0]])
                        scores_rows[i] = r
                    else:
                        r.append(0)
            scores = pd.DataFrame(scores_rows, columns=scores_cols)
            scores.set_index("Name", inplace=True)

            self._scores = scores

        return self._scores

    @property
    def fpaths(self):
        if not self._fpaths:
            dpath = self.fpath.parent.as_posix()
            fpaths = []
            for f in os.listdir(dpath):
                if f.endswith(self.fext):
                    fpath = (Path(dpath) / f).as_posix()
                    wb = load_workbook(fpath, read_only=True)
                    sheet = wb.active
                    test_t1 = self.get_test_t(sheet)
                    if test_t1:
                        test_t1 = test_t1[1]

                    if test_t1:
                        fpaths.append([fpath, test_t1])

                    else:
                        wb.close()
                        sheet = None
                        test_t1 = datetime.fromtimestamp(
                            os.path.getctime(fpath)
                        )
                        fpaths.append([fpath, test_t1])
            self._fpaths = fpaths

            if len(self._fpaths) < 1:
                return None

        self._fpaths = sorted(self._fpaths, key=lambda f: (f[1], f[0]))

        return self._fpaths

    @property
    def grade(self):
        value = self.name.split("/")
        if len(value) > 2:
            value = value[0]
        else:
            return None
        return value

    @property
    def subject(self):
        value = self.name.split("/")
        if len(value) > 2:
            value = value[1]
        else:
            return None
        return value

    @property
    def short_name_m2(self):
        if not self._short_name_m2:
            if len(self.fpaths) > 1:
                name, __ = self.fpaths[-2]
                self._short_name_m2 = Path(name).stem
            else:
                return None

        return self._short_name_m2

    @property
    def test_t(self):
        if not self._test_t:
            self._test_t = self.get_test_t(self.sheet0)

        return self._test_t

    def get_cell_time(self, value):
        value = str(value)
        time = (
            (
                datetime.strptime(value, "%Y/%m/%d %H：%M")
                if "：" in value
                else datetime.strptime(value, "%Y/%m/%d %H:%M")
            )
            if "/" in value
            else (
                (
                    datetime.strptime(value, "%Y%m%d %H：%M")
                    if "：" in value
                    else datetime.strptime(value, "%Y%m%d %H:%M")
                )
                if " " in value
                else datetime.strptime(value, "%Y%m%d%H%M")
            )
        )

        return time

    def get_test_t(self, sheet):

        test_t = None
        test_t0 = sheet.cell(1, 2).value
        test_t1 = sheet.cell(1, 5).value
        time_from_cell_value = self.get_cell_time
        if test_t0:
            try:
                test_t0 = time_from_cell_value(test_t0)
            except:
                print_error(
                    _(
                        "Failed to get examination " + 'start time from "{0}".'
                    ).format(test_t0)
                )
                return None
        else:
            return None

        if test_t1:
            try:
                test_t1 = time_from_cell_value(test_t1)
            except:
                print_error(
                    _(
                        "Failed to get examination " + 'end time from "{0}".'
                    ).format(test_t1)
                )
        if test_t0 and not test_t1:
            test_t1 = test_t0 + timedelta(minutes=90)
            print_warning(
                _('The examination end time is set to "{0}".').format(
                    test_t1.strftime("%Y/%m/%d %H%M")
                )
            )

        test_t = [test_t0, test_t1]

        return test_t

    @property
    def short_name(self):
        if not self._short_name:
            self._short_name = Path(self.fpath).stem

        return self.short_name

    @property
    def wb(self):
        if not self._wb:
            self._wb = load_workbook(self.fpath)
        return self._wb

    @property
    def sheet0(self):

        if not self._sheet0:
            self._sheet0 = self.wb[self.wb.sheetnames[0]]
        return self._sheet0

    @property
    def scores_m1(self):

        if self._scores_m1 is None:

            fpath = self.fpath
            scores = self.get_scores(fpath)
            self._scores_m1 = scores

        return self._scores_m1

    def get_points(self, question):
        points = question
        if "（" in points:
            points = points.split("（")[1]
        if "(" in points:
            points = points.split("(")[1]
        if "分" in points:
            points = points.split("分")[0]
        if "）" in points:
            points = points.split("）")[0]
        if ")" in points:
            points = points.split(")")[0]
        points = points.strip()

        if str.isnumeric(points.replace(".", "")):
            return float(points)

        return 0

    @property
    def total_points(self):
        if not self._total_points:
            total_points = sum(
                [self.get_points(q) for q in self.question_titles]
            )
            self._total_points = total_points

        return self._total_points

    @property
    def question_titles(self):
        if not self._question_titles:
            self._question_titles = self.get_question_titles(self.scores)

        return self._question_titles

    def get_question_titles(self, scores):
        question_titles = scores.columns.to_list()
        question_titles = question_titles[1:]
        return question_titles

    @property
    def names_fpath(self):
        fpath = self.teacher.dpath / (_("exam_names") + ".txt")
        if not fpath.exists():
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("")
        return fpath

    @property
    def fpath_m2(self):
        if not self._fpath_m2:
            path = self.fpaths[-2][0] if len(self.fpaths) > 1 else None
            self._fpath_m2 = path
        return self._fpath_m2

    @property
    def fpath(self):
        if not self._fpath:
            self._fpath = self.teacher.exam_dpath / (
                Path(self.full_name).as_posix() + self.fext
            )
            if not self._fpath.parent.exists():
                os.makedirs(self._fpath.parent.as_posix(), exist_ok=True)

            if not self._fpath.exists():
                shutil.copy(self.fpath0, self._fpath)
                print_info(
                    _(
                        'Scores spreadsheet "{0}" doesn\'t '
                        + 'exist, spreadsheet "{1}" was '
                        + 'copied to "{0}".'
                    ).format(self._fpath, self.fpath0)
                )

                fpath1 = self.fpath_m2
                name_m2 = self.short_name_m2 or self.no_test_m2_s
                scores_m2 = (
                    self.scores[-1][1] if (not self.scores is None) else None
                )
                names_len = (
                    len(scores_m2) - 1 if not (scores_m2 is None) else None
                )

                wb = self.wb
                sheet = self.sheet0

                sheet.cell(2, 3, name_m2)
                new_names_len = (
                    len(
                        [
                            sheet.cell(r, 1).value
                            for r in range(self.name_index0, sheet.max_row + 1)
                            if sheet.cell(r, 1).value
                        ]
                    )
                    - 1
                )
                if scores_m2:
                    len_diff = names_len - new_names_len
                    if len_diff > 0:
                        sheet.insert_rows(self.name_index0 + 1, len_diff)
                    elif len_diff < 0:
                        sheet.delete_rows(self.name_index0 + 1, -len_diff)

                    for i, (s_name, s_score) in enumerate(scores_m2):
                        sheet.cell(self.name_index0 + i, 1, s_name)
                        sheet.cell(self.name_index0 + i, 3, s_score)

                    print_info(
                        _(
                            "The recent examination scores ({0}) "
                            + 'have been added to "{1}".'
                        ).format(name_m2, fpath)
                        if scores_m2
                        else _("There is no recent tests.")
                    )

                wb.save(fpath)
                print_info(_('Spreadsheet "{0}" has been saved.').format(fpath))
                wb.close()
                sheet = None
                print_info(
                    _(
                        "Please update the question titles "
                        + ", student names "
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
                        + " titles, student names and scores, and I CLOSED "
                        + "the file. "
                        + "(Press any key to continue)"
                    )
                )
                input(">_ ")

        return self._fpath

    @property
    def full_name(self):
        if not self._full_name:
            names = None
            with open(self.names_fpath, "r", encoding="utf-8") as f:
                names = f.read().replace(" ", "").strip().split("\n")
            names = [n for n in names if (len(n) > 0)]
            names_len = len(names)

            name_writed_s = lambda name=None: (
                _(
                    'The examination name "{0}" ' + 'has been saved to "{1}".'
                ).format(name, self.names_fpath)
                if name
                else _('The examination name has been saved to "{0}".').format(
                    self.names_fpath
                )
            )

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
                        [
                            f"{i+1:>{names_len2}} {n}"
                            for i, n in enumerate(names)
                        ]
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
                    with open(self.names_fpath, "w", encoding="utf-8") as f:
                        f.write("\n".join([">" + name_i] + names))
                    name0 = name_i
                    print_info(name_writed_s(name0))

                self._full_name = name0

            else:
                print_info(
                    _(
                        "Hello~ tell {0} the examination" + " name, please!"
                    ).format(app_name)
                )
                for i in range(0, 3):
                    name0 = input(">_ ").replace(" ", "")
                    if len(name0) > 0:
                        with open(self.names_fpath, "w", encoding="utf-8") as f:
                            f.write(">" + self._full_name)
                        print_info(name_writed_s(name0))
                        self._full_name = name0
                        break
                    else:
                        print_error(_("Unexpected value was got."))
                    if i > 2:
                        print_error(_("Unexpected value was got." + " Exit."))
                        exit()

        if self._full_name.startswith("/"):
            self._full_name = re.sub(r"^/+", "", self._full_name)
        if self._full_name.startswith("\\"):
            self._full_name = re.sub(r"^\\+", "", self._full_name)
        if ".." in self._full_name:
            self._full_name = re.sub("..", "", self._full_name)

        if "/" in self._full_name:
            dpath = (self.teacher.exam_dpath / Path(self._full_name)).parent
            if not dpath.exists():
                os.makedirs(dpath, exist_ok=True)

        return self._full_name

    @full_name.setter
    def full_name(self, value):
        exam_dpath = self.teacher.exam_dpath.as_posix()
        value = Path(value).as_posix()
        if exam_dpath in value:
            value = value.replace(exam_dpath, "")
        value = os.path.splitext(value)[0]
        self._full_name = value


# The end.
