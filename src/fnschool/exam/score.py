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
        self._name_m1 = None
        self._test_t = None
        self._fpath = None
        self._fpath_m1 = None
        self._fpaths = None
        self._scores = None
        self._wb = None
        self._total_points = None
        self._sheet0 = None
        self._prev_scores = None
        self.p_path_key = _("scores_parent_directory")
        self._question_titles = None
        self.fext = ".xlsx"
        self.no_test_m1_s = _("No recent tests")
        self.name_index0 = 3
        self.question_index0 = 4
        self.fpath_is_new = False

        pass

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

        print(self.prev_scores)

    @property
    def prev_scores(self):
        if not self._prev_scores:
            scores = []
            fpaths = (
                fpaths[:-2] if self.fpath in self.fpaths else self.fpaths[:-1]
            )
            if len(fpaths) < 1:
                return None

            for f, __ in fpaths:
                name = Path(f).stem
                wb = load_workbook(f)
                sheet = wb[wb.sheetnames[0]]

                headers = [
                    sheet.cell(2, c).value
                    for c in range(1, sheet.max_column + 1)
                    if sheet.cell(2, c).value
                ]
                max_col0 = headers.index("考试纪律") + 1
                print(max_col0)
                sub_scores = [
                    (
                        sheet.cell(r, 1).value,
                        sum(
                            [
                                float(sheet.cell(r, c).value)
                                for c in range(self.question_index0,max_col0 )
                                if sheet.cell(r, c).value
                            ]
                        )
                        - (
                            float(sheet.cell(r, max_col0).value)
                            if sheet.cell(r, max_col0).value
                            else 0
                        )
                    )
                    for r in range(self.name_index0, sheet.max_row + 1)
                    if (
                        sheet.cell(r, 2).value
                        and not "平均分" in sheet.cell(r,1).value
                    )
                ]
                scores.append((name, sub_scores))
            self._prev_scores = scores

        return self._prev_scores

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
    def name_m1(self):
        if not self._name_m1:
            if len(self.fpaths) > 1:
                name, __ = self.fpaths[-1]
                self._name_m1 = Path(name).stem
            else:
                return None

        return self._name_m1

    @property
    def test_t(self):
        if not self._test_t:
            self._test_t = self.get_test_t(self.sheet0)

        return self._test_t

    def get_test_t(self, sheet):

        test_t = None
        test_t0 = sheet.cell(1, 2).value
        test_t1 = sheet.cell(1, 5).value
        time_from_cell_value = lambda value: (
            datetime.strptime(str(value), "%Y/%m%d %H:%M")
            if "/" in value
            else datetime.strptime(str(value), "%Y%m%d%H%M")
        )

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
                    test_t1.strftime("%Y/%m/%d %H:%M")
                )
            )

        test_t = [test_t0, test_t1]

        return test_t

    @property
    def name0(self):
        if not self._name0:
            self._name0 = Path(self.fpath).stem

        return self._name0

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
    def scores(self):

        if self._scores is None:

            fpath = self.fpath
            fpaths = self.fpaths
            fpath1 = self.fpath_m1
            name_m1 = self.name_m1 or self.no_test_m1_s
            scores_m1 = self.prev_scores[-1][1] if self.prev_scores else None
            names_len = len(scores_m1) - 1 if scores_m1 else None

            wb = self.wb
            sheet = self.sheet0

            sheet.cell(2, 3, self.name_m1)
            sheet_names_len = (
                len(
                    [
                        sheet.cell(r, 1).value
                        for r in range(self.name_index0, sheet.max_row + 1)
                        if sheet.cell(r, 1).value
                    ]
                )
                - 1
            )
            len_diff = names_len - sheet_names_len
            if len_diff > 0:
                sheet.insert_rows(self.name_index0 + 1, len_diff)
            elif len_diff < 0:
                sheet.delete_rows(self.name_index0 + 1, -len_diff)

            if self.fpath_is_new:
                for i, (s_name, s_score) in enumerate(scores_m1):
                    sheet.cell(self.name_index0 + i, 1, s_name)
                    sheet.cell(self.name_index0 + i, 3, s_score)
            else:
                for row_index in range(self.name_index0, sheet.max_row + 1):
                    name = sheet.cell(row_index, 1).value
                    if name:
                        score = 0
                        if scores_m1:
                            score = (
                                [
                                    s_score
                                    for s_name, s_score in scores_m1
                                    if s_name == name
                                ]
                            )
                            score = score[0] if len(score)>0 else 0
                        sheet.cell(row_index, 3, score)

            if name_m1:
                print_info(
                    _(
                        "The recent examination scores ({0}) "
                        + 'have been added to "{1}".'
                    ).format(name_m1, fpath)
                    if scores_m1
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

            scores = pd.read_excel(fpath, skiprows=[0])

            scores.rename(columns={scores.columns[0]: "姓名"}, inplace=True)
            scores.drop(scores.tail(1).index, inplace=True)
            scores.set_index("姓名", inplace=True)
            scores["考试纪律"] = scores["考试纪律"].fillna(0)
            question_titles = self.get_question_titles(scores)
            scores["总分"] = scores.loc[:, question_titles].sum(axis=1)

            self._scores = scores

        return self._scores

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
        i0, i1 = question_titles.index(
            self.name_m1 or self.no_test_m1_s
        ), question_titles.index("考试纪律")
        question_titles = question_titles[i0 + 1 : i1]
        return question_titles

    @property
    def name_fpath(self):
        fpath = self.teacher.dpath / (_("exam_names") + ".txt")
        if not fpath.exists():
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("")
        return fpath

    @property
    def fpath_m1(self):
        if not self._fpath_m1:
            path = self.fpaths[-1][0] if len(self.fpaths) > 1 else None
            self._fpath_m1 = path
        return self._fpath_m1

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
                print_info(
                    _(
                        'Scores spreadsheet "{0}" doesn\'t '
                        + 'exist, spreadsheet "{1}" was '
                        + 'copied to "{0}".'
                    ).format(self._fpath, self.fpath0)
                )
                sef.fpath_is_new = True

        return self._fpath

    @property
    def name(self):
        if not self._name:
            names = None
            with open(self.name_fpath, "r", encoding="utf-8") as f:
                names = f.read().replace(" ", "").strip().split("\n")
            names = [n for n in names if (len(n) > 0)]
            names_len = len(names)

            name_writed_s = lambda name=None: (
                _(
                    'The examination name "{0}" ' + 'has been saved to "{1}".'
                ).format(name, self.name_fpath)
                if name
                else _('The examination name has been saved to "{0}".').format(
                    self.name_fpath
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
                    with open(self.name_fpath, "w", encoding="utf-8") as f:
                        f.write("\n".join([">" + name_i] + names))
                    name0 = name_i
                    print_info(name_writed_s(name0))

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
                        with open(self.name_fpath, "w", encoding="utf-8") as f:
                            f.write(">" + self._name)
                        print_info(name_writed_s(name0))
                        self._name = name0
                        break
                    else:
                        print_error(_("Unexpected value was got."))
                    if i > 2:
                        print_error(_("Unexpected value was got." + " Exit."))
                        exit()

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

    @name.setter
    def name(self, value):
        exam_dpath = self.teacher.exam_dpath.as_posix()
        if exam_dpath in value:
            value = value.replace(exam_dpath, "")
        value = os.path.splitext(value)[0]
        self._name = value


# The end.
