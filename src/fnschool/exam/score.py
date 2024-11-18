import os
import sys
import time
from fnschool import *
from fnschool.exam import *
from fnschool.exam.path import *
from fnschool.exam.teacher import *
from fnschool.exam.email import Email as FnEmail


class Score:
    def __init__(
        self,
    ):
        self._full_name = None
        self._teacher = None
        self.fpath0 = score_fpath0
        self._sclass = None
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
        self._sheet0 = None
        self._total_points = None
        self._scores = None
        self.p_path_key = _("scores_parent_directory")
        self._question_titles = None
        self.fext = ".xlsx"
        self.no_test_m2_s = _("No recent tests")
        self.name_index0 = 4
        self.question_index0 = 4
        self.points_index0 = self.question_index0 - 1
        self._test_names = None
        self._astudent_names = None
        self._student_names = None
        self._src_dpath = None
        self.average_points_s = _("Average")
        self.plot_alpha0 = 0.16
        self.discipline_s = _("Discipline Points")
        self.name_s = _("Student Name")
        self._scores_m1_img_afpaths = None
        self._scores_img_afpaths = None
        self._scores_img_fpaths = None
        self._email = None
        self._sclass_dpath = None

        pass

    @property
    def email(self):
        if not self._email:
            email = FnEmail(self)
            self._email = email
        return self._email

    @property
    def test_names(self):
        if not self._test_names:
            scores = self.scores
            test_names = scores.columns.to_list()
            self._test_names = test_names
        return self._test_names

    @property
    def astudent_names(self):
        if not self._astudent_names:
            scores = self.scores
            astudent_names = scores.index.to_list()
            self._astudent_names = astudent_names
        return self._astudent_names

    @property
    def student_names(self):
        if not self._student_names:
            names = self.astudent_names
            if self.average_points_s in names:
                names.remove(self.average_points_s)
            self._student_names = names
        return self._student_names

    @property
    def src_dpath(self):
        return self.get_src_dpath()

    def get_src_dpath(self, fpath=None):
        if fpath or not self._src_dpath:
            src_dpath = fpath or self.fpath
            src_dpath = Path(os.path.splitext(src_dpath)[0])
            if fpath:
                return src_dpath
            self._src_dpath = src_dpath
        return self._src_dpath

    def get_rotation(self, xticks):
        locs, labels = xticks

        boxes = [l.get_window_extent().get_points() for l in labels]
        x0, x1 = boxes[0][0][0], boxes[-1][0][0]
        label_w = (x1 - x0) / (len(labels))
        label_hx = max([b[-1][1] - b[0][1] for b in boxes])
        rotation = math.degrees(math.sin(label_hx / label_w))
        return rotation

    def plot(self):
        print_info(
            (
                _(
                    "Generate the scores and scoring "
                    + 'rate plots now ? (Yes: "Y","y")'
                )
                if len(self.scores.columns) > 1
                else _(
                    "Generate the scoring " + 'rate plots now ? (Yes: "Y","y")'
                )
            )
        )
        p_input = input0()
        if p_input and p_input in "Yy":
            if len(self.scores.columns) > 1:
                self.plot_scores()
            self.plot_scores_m1()

    def get_scores_img_fpath(self, student_name=None):

        img_path = (
            self.src_dpath
            / (
                (
                    _("scores_of_all_students")
                    if not student_name
                    else (
                        _("scores_of_{0}").format(student_name)
                        if student_name != self.average_points_s
                        else _("average_scores")
                    )
                )
                + ".png"
            )
        ).as_posix()
        return img_path

    def print_summary(self):
        scores_m1 = self.scores_m1.copy()
        scores_m1_t = scores_m1[scores_m1.columns[0]]
        scores_m1_index = scores_m1.index.to_list()
        scores_m1_index_lenx = max([len(i) for i in scores_m1_index])
        if scores_m1_index_lenx == 3:
            scores_m1_index = [
                (i if len(i) > 2 else i[0] + "  " + i[1])
                for i in scores_m1_index
            ]
            scores_m1_t = pd.Series(scores_m1_t.values, index=scores_m1_index)
        scores_m1_t = scores_m1_t.sort_values(ascending=False)
        scores_m1_t_len2 = len(str(scores_m1_t.size))
        scores_m1_t_s = sqr_slist(
            [
                f"{i+1:>{scores_m1_t_len2}}. {s_name} ({s_point:.2f})"
                for i, (s_name, s_point) in enumerate(scores_m1_t.items())
            ]
        )
        sep = get_random_sep_char() * max(
            [get_len(s) for s in scores_m1_t_s.split("\n")]
        )
        summary_s = (
            "\n"
            + _("Summary of {0}:").format(self.full_name)
            + "\n"
            + sep
            + "\n"
            + _("Scores:")
            + "\n"
            + scores_m1_t_s
            + "\n"
            + sep
        )
        print_info(summary_s)

        pass

    @property
    def scores_img_fpaths(self):
        if not self._scores_img_fpaths:
            fpaths = []
            for name in self.student_names:
                fpaths.append(
                    [
                        name,
                        self.get_scores_m1_img_fpath(name),
                        self.get_scores_img_fpath(name),
                    ]
                )
            self._scores_img_fpaths = fpaths
        return self._scores_img_fpaths

    @property
    def scores_img_afpaths(self):
        if not self._scores_img_afpaths:
            self._scores_img_afpaths = [
                [name, self.get_scores_img_fpath(name)]
                for name in self.astudent_names
            ]
        return self._scores_img_afpaths

    def plot_scores(self, max_test_num=None):
        scores = self.scores

        scores_m1 = self.scores_m1.copy()
        scores_m1_d = scores_m1.loc[:, scores_m1.columns[1]]
        max_test_num = max_test_num or scores.columns.size
        test_names = self.test_names
        img_saved_s = _('[{0}] "{1}" {2}has been saved.')
        img_fpaths = [f for __, f in self.scores_img_afpaths] + [
            self.get_scores_img_fpath()
        ]

        img_paths_lenx = max(get_len(f) for f in img_fpaths)

        i_index = 0
        img_fpaths_len = len(img_fpaths)
        img_fpaths_len2 = len(str(img_fpaths_len))
        labelrotation = None
        for student_name, s_scores in scores.iterrows():
            comment = self.get_comment(student_name)
            discipline_points = scores_m1_d.loc[student_name]
            student_name0 = (
                student_name
                if len(student_name) > 2
                else (student_name[0] + "　" + student_name[1])
            )

            img_fpath = self.get_scores_img_fpath(student_name)
            img_fpath_len_diff = (
                img_paths_lenx - get_zh_CN_chars_len(img_fpath) - len(img_fpath)
            )

            s_scores = s_scores[:max_test_num]
            plt.plot(range(s_scores.size), s_scores)
            plt.title(
                _("The scores of Student {0}").format(student_name0)
                if not student_name == self.average_points_s
                else _("The average scores")
            )
            xticks = plt.xticks(range(s_scores.size), self.test_names)

            if not labelrotation:
                labelrotation = self.get_rotation(xticks)
            plt.tick_params(axis="x", labelrotation=labelrotation)

            plt.xlabel(_("Examination names of {0}").format(self.subject))
            plt.ylabel(
                (
                    _("Examination Points " + "({0} points in total)")
                    if self.total_points != 1.0
                    else _("Examination Points " + "({0} point in total)")
                ).format(self.total_points)
            )
            for test_name, point in s_scores.items():
                plt.text(
                    *(test_names.index(test_name), point),
                    round(point, 2),
                    va="bottom",
                    bbox=dict(
                        facecolor="red",
                        alpha=self.plot_alpha0,
                        boxstyle="round",
                    ),
                )

            comment_value = ""

            if comment:
                comment_value += comment

            if not discipline_points == 0.0:
                comment_value += ("\n" if comment else "") + (
                    _("Discipline point: {0}.")
                    if discipline_points == 1.0
                    else _("Discipline points: {0}.")
                ).format(discipline_points)

            if comment_value:
                plt.text(
                    *(0, s_scores.max()),
                    comment_value,
                    ha="left",
                    va="top",
                    bbox=dict(
                        facecolor="white",
                        alpha=0.5,
                        boxstyle="round",
                        edgecolor="red",
                    ),
                )

            plt.savefig(img_fpath, bbox_inches="tight")
            print_info(
                img_saved_s.format(
                    f"{i_index+1:>{img_fpaths_len2}}/{img_fpaths_len}",
                    img_fpath,
                    " " * img_fpath_len_diff,
                )
            )
            plt.cla()
            i_index += 1

        plt.cla()
        student_scores_img_fpath = img_fpaths[-1]
        scores0 = scores.T
        scores0.columns.name = self.name_s
        img_fpath_len_diff = (
            img_paths_lenx
            - get_zh_CN_chars_len(student_scores_img_fpath)
            - len(student_scores_img_fpath)
        )

        scores0.plot()
        plt.title(_("The scores of all students"))
        xticks = plt.xticks(range(s_scores.size), self.test_names)

        if not labelrotation:
            labelrotation = self.get_rotation(xticks)
        plt.tick_params(axis="x", labelrotation=labelrotation)

        plt.xlabel(_("Examination names of {0}").format(self.subject))
        plt.ylabel(
            (
                _("Examination Points " + "({0} points in total)")
                if self.total_points != 1.0
                else _("Examination Points " + "({0} point in total)")
            ).format(self.total_points)
        )
        plt.savefig(student_scores_img_fpath, bbox_inches="tight")
        print_info(
            img_saved_s.format(
                f"{i_index+1:>{img_fpaths_len2}}/{img_fpaths_len}",
                student_scores_img_fpath,
                " " * img_fpath_len_diff,
            )
        )
        plt.cla()

    def get_scores_m1_img_fpath(self, student_name):
        img_fpath = (
            self.src_dpath
            / (
                (
                    _("scoring_rate_of_{0}").format(student_name)
                    if not student_name == self.average_points_s
                    else _("average_scoring_rate")
                )
                + ".png"
            )
        ).as_posix()

        return img_fpath

    @property
    def scores_m1_img_afpaths(self):
        if not self._scores_m1_img_afpaths:
            fpaths = [
                [v, self.get_scores_m1_img_fpath(v)]
                for v in self.astudent_names
            ]
            self._scores_m1_img_afpaths = fpaths
        return self._scores_m1_img_afpaths

    def plot_scores_m1(self):
        scores_m1 = self.scores_m1
        scores_m1.loc[self.average_points_s] = scores_m1.mean(axis=0)
        scores_m1_t = scores_m1.loc[:, scores_m1.columns[0]]
        scores_m1_d = scores_m1.loc[:, scores_m1.columns[1]]
        scores_m1_q = scores_m1.loc[:, scores_m1.columns[2:]]
        scores_m1_q = scores_m1_q.astype(float)
        img_saved_s = _('[{0}] "{1}" {2}has been saved.')

        for student_name, q_points in scores_m1_q.iterrows():
            for q_title, q_point in q_points.items():
                q_point_t = self.get_points(q_title)
                scores_m1_q.loc[student_name, q_title] = round(
                    q_point * 100 / q_point_t, 1
                )
        img_fpaths = [f for __, f in self.scores_m1_img_afpaths]
        img_fpaths_lenx = max(get_len(f) for f in img_fpaths)

        labelrotation = None
        i_index = 0
        img_fpaths_len = len(img_fpaths)
        img_fpaths_len2 = len(str(img_fpaths_len))
        for student_name, q_point_rates in scores_m1_q.iterrows():

            s_total_points = scores_m1_t.loc[student_name]

            student_name0 = (
                student_name
                if len(student_name) > 2
                else (student_name[0] + "　" + student_name[1])
            )

            img_fpath = self.get_scores_m1_img_fpath(student_name)
            img_fpath_len_diff = (
                img_fpaths_lenx
                - get_zh_CN_chars_len(img_fpath)
                - len(img_fpath)
            )

            img = plt.bar(range(q_point_rates.size), q_point_rates)
            plt.title(
                (
                    _("The scoring rate of Student {0} ({1})").format(
                        student_name0, f"{s_total_points}/{self.total_points}"
                    )
                    if student_name != self.average_points_s
                    else _("The average scoring rate ({0})").format(
                        f"{s_total_points:.2f}/{self.total_points}"
                    )
                )
            )
            xticks = plt.xticks(range(q_point_rates.size), self.question_titles)

            if not labelrotation:
                labelrotation = self.get_rotation(xticks)
            plt.tick_params(axis="x", labelrotation=labelrotation)

            showed_test_name = f"{self.subject}/{self.short_name}"
            plt.xlabel(
                _("Question titles of {0} ({1})").format(
                    showed_test_name,
                    (
                        _("{0} point in total, ")
                        if self.total_points == 1
                        else _("{0} points in total, ")
                    ).format(self.total_points)
                    + (
                        _("{0} point got")
                        if s_total_points == 1
                        else _("{0} points got")
                    ).format(s_total_points),
                )
            )

            plt.ylabel(_("Scoring rate(%)"))
            for q_title, s_rate in q_point_rates.items():
                plt.text(
                    *(self.question_titles.index(q_title), s_rate),
                    f"{s_rate}%",
                    va="bottom",
                    ha="center",
                    bbox=dict(
                        facecolor="red",
                        alpha=self.plot_alpha0,
                        boxstyle="round",
                    ),
                )

            plt.savefig(img_fpath, bbox_inches="tight")
            print_info(
                img_saved_s.format(
                    f"{i_index+1:>{img_fpaths_len2}}/{img_fpaths_len}",
                    img_fpath,
                    " " * img_fpath_len_diff,
                )
            )
            plt.cla()
            i_index += 1
        i_index = 0

    def get_comment(self, student_name):
        comment = _("comment:") + "\n"
        for row in self.sheet0.iter_rows():
            if student_name == row[0].value:
                if not row[0].comment:
                    return None
                comment += row[0].comment.text
                return comment

        return None

    @property
    def dpath(self):
        if not self._dpath:
            self._dpath = self.fpath.parent
        print(self._dpath)
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
        __ = self.scores
        self.plot()
        self.print_summary()
        self.email.send_scores()
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

        self.full_name = filename

        self.plot()

    def get_scores(self, fpath):
        if not Path(fpath).exists():
            return None

        discipline_s = "考试纪律"
        scores = pd.read_excel(fpath, skiprows=[0, 2])
        scores.rename(columns={scores.columns[0]: self.name_s}, inplace=True)
        scores.dropna(subset=[self.name_s], inplace=True)
        scores.set_index(self.name_s, inplace=True)
        scores[discipline_s] = scores[discipline_s].fillna(0)
        point_cols = scores.columns[self.points_index0 :].to_list()
        scores["总分"] = (
            scores.loc[:, point_cols].sum(axis=1) + scores[discipline_s]
        )
        scores.drop([scores.columns[1]], axis=1, inplace=True)
        scores = scores.loc[:, ~scores.columns.str.contains("^Unnamed")]

        return scores

    def edit_test_m1(self):
        fpaths = self.get_fpaths()
        fpath_m1, __ = fpaths[-1]
        print_warning(
            _(
                "Would you like to edit \"{0}\" ? (\"Yes\": 'Y' or 'y'. "
                + "Default: No)"
            ).format(fpath_m1)
        )
        edit_yn = input0()
        if edit_yn and edit_yn in "Yy":
            open_path(fpath_m1)
            print_info(
                _(
                    "Ok, I have edited and closed it? (Enter any key "
                    + "to continue)"
                )
            )
            input0()
            pass
        pass

    @property
    def scores(self):
        if self._scores is None:
            if not self.fpath == self.fpaths[-1][0]:
                self.edit_test_m1()
            fpaths = self.fpaths[::-1]
            if len(fpaths) < 1:
                return None

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
                        s_points = f_scores.loc[s_name, f_scores.columns[0]]
                        s_points = 0 if pd.isna(s_points) else s_points
                        r.append(s_points)
                        scores_rows[i] = r
                    else:
                        r.append(0)

            scores = pd.DataFrame(scores_rows, columns=scores_cols)

            scores.set_index("Name", inplace=True)
            scores.loc[self.average_points_s] = scores.mean(axis=0)

            self._scores = scores[scores.columns[::-1]]

        return self._scores

    @scores.deleter
    def scores(self):
        self._scores = None
        del self.total_points
        del self.scores_m1

    @property
    def fpaths(self):
        fpaths = self.get_fpaths()
        return fpaths
        pass

    @fpaths.setter
    def fpaths(self, paths):
        self._fpaths = paths
        pass

    def get_fpaths(self, dpath=None):
        fpath_time = None
        if not self._fpaths:
            dpath = dpath or self.fpath.parent.as_posix()
            fpaths = []
            fpath_time = None
            for f in os.listdir(dpath):
                if f.endswith(self.fext):
                    fpath = (Path(dpath) / f).as_posix()
                    wb = load_workbook(fpath, read_only=True)
                    sheet = wb.active
                    test_t1 = self.get_test_t(sheet)
                    if test_t1:
                        test_t1 = test_t1[1]
                    else:
                        test_t1 = get_file_ctime(fpath)

                    if fpath == self.fpath.as_posix():
                        fpath_time = test_t1

                    fpaths.append([fpath, test_t1])
            self._fpaths = fpaths
            if len(self._fpaths) < 1:
                return None

        self._fpaths = sorted(self._fpaths, key=lambda f: (f[1], f[0]))
        if fpath_time:
            self._fpaths = [[f, t] for f, t in fpaths if t <= fpath_time]
        return self._fpaths

    @property
    def sclass(self):
        if not self._sclass:
            value = self.full_name.split("/")
            if len(value) > 2:
                value = value[0]
            else:
                return None
            self._sclass = value
        return self._sclass

    @property
    def sclass_dpath(self):
        if not self._sclass_dpath:
            sclass_dpath = self.teacher.exam_dpath / self.sclass
            if not sclass_dpath.exists():
                os.makedirs(sclass_dpath, exist_ok=True)
            self._sclass_dpath = sclass_dpath
        return self._sclass_dpath

    @property
    def subject(self):
        value = self.full_name.split("/")
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
        value = re.sub(r"\s+", " ", value)
        time = (
            (
                datetime.strptime(value, "%Y/%m/%d %H：%M")
                if "：" in value
                else (
                    datetime.strptime(value, "%Y/%m/%d %H:%M")
                    if ":" in value
                    else datetime.strptime(value, "%Y/%m/%d %H%M")
                )
            )
            if "/" in value
            else (
                (
                    datetime.strptime(value, "%Y%m%d %H：%M")
                    if "：" in value
                    else (
                        datetime.strptime(value, "%Y%m%d %H:%M")
                        if ":" in value
                        else datetime.strptime(value, "%Y%m%d %H%M")
                    )
                )
                if " " in value
                else datetime.strptime(value, "%Y%m%d%H%M")
            )
        )

        return time

    def get_test_t(self, sheet, interval=90):

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
        else:
            pass

        if test_t0 and not test_t1:
            test_t1 = test_t0 + timedelta(minutes=interval)
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

        return self._short_name

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
            scores_m1 = scores
            scores_m1.fillna(0, axis=1, inplace=True)
            scores_m1.loc[self.average_points_s] = scores_m1.mean(axis=0)
            self._scores_m1 = scores_m1

        return self._scores_m1

    @scores_m1.deleter
    def scores_m1(self):
        self._scores_m1 = None

    def get_points(self, question):
        points = question
        if "（" in points:
            points = points.split("（")[-1]
        if "(" in points:
            points = points.split("(")[-1]
        if "分" in points:
            points = points.split("分")[-2]
        if "）" in points:
            points = points.split("）")[-2]
        if ")" in points:
            points = points.split(")")[-2]
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

    @total_points.deleter
    def total_points(self):
        self._total_points = None

    @property
    def question_titles(self):
        if not self._question_titles:
            self._question_titles = self.get_question_titles(self.scores_m1)

        return self._question_titles

    def get_question_titles(self, scores):
        question_titles = scores.columns.to_list()
        question_titles = [
            q
            for q in question_titles
            if (
                ("(" in q or "（" in q)
                and bool(
                    re.search(
                        r"\d",
                        q.split("(")[-1]
                        .split("（")[-1]
                        .split(")")[0]
                        .split("）")[0],
                    )
                )
            )
        ]
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
            fpath = self.teacher.exam_dpath / (
                Path(self.full_name).as_posix() + self.fext
            )
            if not fpath.parent.exists():
                os.makedirs(fpath.parent.as_posix(), exist_ok=True)

            if not fpath.exists():
                dpath = fpath.parent.as_posix()
                self.fpath = fpath
                fpaths = self.get_fpaths(dpath)
                self.fpath = None
                scores = None
                if fpaths:
                    self.fpath, __ = fpaths[-1]
                    scores = self.scores
                    self.fpath = None
                    self.fpaths = None
                shutil.copy(self.fpath0, fpath)

                print_info(
                    _(
                        'Scores spreadsheet "{0}" doesn\'t '
                        + 'exist, spreadsheet "{1}" was '
                        + 'copied to "{0}".'
                    ).format(fpath, self.fpath0)
                )

                name_m2 = self.short_name_m2 or self.no_test_m2_s

                scores_m2 = (
                    scores[scores.columns[-2]]
                    if not scores is None and (len(scores.columns) > 1)
                    else None
                )

                if not scores_m2 is None:
                    scores_m2 = scores_m2.copy()
                    scores_m2.drop(
                        [self.average_points_s], axis=0, inplace=True
                    )

                wb = load_workbook(fpath)
                sheet = wb[wb.sheetnames[0]]
                sheet.cell(2, 3, name_m2)

                if not scores_m2 is None:
                    r_index = 0
                    for i, (s_name, s_score) in enumerate(scores_m2.items()):
                        sheet.cell(self.name_index0 + i, 1, s_name)
                        sheet.cell(self.name_index0 + i, 3, s_score)
                        r_index = self.name_index0 + i

                    for row_index in range(r_index + 1, sheet.max_row + 1):
                        sheet.cell(row_index, 1, "")
                        sheet.cell(row_index, 3, "")

                    print_info(
                        _(
                            "The recent examination scores ({0}) "
                            + 'have been added to "{1}".'
                        ).format(name_m2, fpath)
                        if not scores_m2 is None
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
                input0()

                y_input_n = 64
                for i in range(y_input_n):
                    open_path(fpath)
                    print_warning(
                        _(
                            "Ok, I have updated the question"
                            + " titles, student names and scores."
                            + " (Press any key to continue)"
                        )
                    )
                    input0()
                    wb = load_workbook(fpath)
                    sheet = wb[wb.sheetnames[0]]

                    total_points = sum(
                        [
                            self.get_points(q)
                            for q in [
                                sheet.cell(2, c).value
                                for c in range(1, sheet.max_column + 1)
                            ]
                            if (q and ("(" in q or "（" in q))
                        ]
                    )
                    print_warning(
                        (
                            _("Is the total score {0} points?")
                            if total_points != 1.0
                            else _("Is the total score {0} point?")
                        ).format(self.total_points)
                        + _(' (Yes: "Y","y")')
                    )
                    y_input = input0()
                    if y_input and y_input in "Yy":
                        del self.scores
                        break
                    else:
                        wb.close()
                        sheet = None
                    if i >= y_input_n:
                        exit()

            self._fpath = fpath

        src_dpath = Path(self.get_src_dpath(self._fpath))
        if not src_dpath.exists():
            os.makedirs(src_dpath, exist_ok=True)

        return self._fpath

    @fpath.setter
    def fpath(self, path):
        self._fpath = path

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
                    n_input = input0().replace(" ", "")
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
                        "Hello~ tell {0} the examination"
                        + " name, please!"
                        + " (e.g: Class 5(1)/English Volume "
                        + "1/Unit 1 Testing)"
                    ).format(app_name)
                )
                for i in range(0, 3):
                    name0 = input0().replace(" ", "")
                    if len(name0) > 0:
                        with open(self.names_fpath, "w", encoding="utf-8") as f:
                            f.write(">" + name0)
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
            if value.startswith("/"):
                value = re.sub(r"^/+", "", value)
            if value.startswith("\\"):
                value = re.sub(r"^\\+", "", value)
            if ".." in value:
                value = re.sub("..", "", value)

        value = os.path.splitext(value)[0]
        self._full_name = value


# The end.
