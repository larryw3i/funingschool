import smtplib
import email.utils
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase

from redmail import EmailSender

import shutil
from fnschool import *
from fnschool.exam import *
from fnschool.exam.path import *


class Email:
    def __init__(self, score=None):
        self._fpath = None
        self.score = score
        self._teacher = None
        self.fext0 = ".xlsx"
        self._wb = None
        self._sheet0 = None
        self._email = None
        self._html = None
        self.host_key = _("smtp_host")
        self.port_key = _("smtp_port")
        self.user_name_key = _("smtp_user_name")
        self.passw0rd_key = _("smtp_password")
        self._chaperones = None
        pass

    @property
    def chaperones(self):
        if not self._chaperones:
            _chaperones0 = [
                _("self"),
                _("dad"),
                _("mum"),
                _("father’s father"),
                _("father's mother"),
                _("mother's father"),
                _("mother's mother"),
                _("father's older brother"),
                _("father's younger brother"),
                _("father's sister"),
                _("father's sister's husband"),
                _("mother's sister"),
                _("mother's sister's husband"),
                _("relative"),
                _("friend"),
                _("parent"),
                _("chaperone"),
            ]
            _chaperones = _chaperones0 if is_zh_CN else _chaperones0
            self._chaperones = _chaperones
        return self._chaperones
        pass

    @property
    def html(self):
        if not self._html:
            html = None
            with open(
                self.teacher.scores_html_fpath, "r+", encoding="utf-8"
            ) as f:
                html = f.read()
            self._html = html
        return self._html

    @property
    def host(self):
        h = self.teacher.get_profile(
            self.host_key,
            info=_("Tell {0} your SMTP server host, please!").format(app_name),
        )
        return h

    @property
    def port(self):
        p = self.teacher.get_profile(
            self.port_key,
            info=_("Tell {0} your SMTP server port, please!").format(app_name),
        )
        p = int(p)
        return p

    @property
    def user_name(self):
        u = self.teacher.get_profile(
            self.user_name_key,
            info=_("Tell {0} your user name at SMTP server, please!").format(
                app_name
            ),
        )
        return u

    @property
    def passw0rd(self):
        p = self.teacher.get_profile(
            self.passw0rd_key,
            _("Tell {0} your password for SMTP server, please!").format(
                app_name
            ),
        )
        return p

    @property
    def email(self):
        if not self._email:
            from smtplib import SMTP_SSL, SMTP, LMTP

            email = EmailSender(
                host=self.host,
                port=self.port,
                username=self.user_name,
                password=self.passw0rd,
                use_starttls=True,
            )
            self._email = email
        return self._email

    def send_scores(self):
        print_info(
            _(
                "Hey! {0}, do you want to "
                + "send these scores of students"
                + " to chaperones? (Yes: 'Y','y')"
            ).format(self.teacher.name)
        )
        s_input = input0()
        if s_input and s_input in "Yy":
            scores_img_fpaths = self.score.scores_img_fpaths
            msg_subject = _('The scores of Test "{0}"').format(
                self.score.full_name
            )

            student_names = self.score.student_names
            scores_img_fpaths_len = len(scores_img_fpaths)
            scores_img_fpaths_len2 = len(str(scores_img_fpaths_len))
            student_names_lenx = max([get_len(n) for n in student_names])
            chaperone_lenx = 0

            get_full_chaperone = lambda chaperone: (
                student_name
                + (
                    ""
                    if chaperone == self.chaperones[0]
                    else _("'s") + chaperone
                )
                if is_zh_CN
                else (
                    student_name + "' " + chaperone
                    if student_name.endswith("s")
                    else student_name + "s' " + chaperone
                )
            )
            get_full_chaperone0 = lambda chaperone, email: (
                f"{email}({chaperone})"
            )

            for student_name, __, __0 in scores_img_fpaths:
                chaperones_emails = self.get_chaperones_emails(student_name)
                for chaperone, cemails in chaperones_emails:
                    for cemail in cemails:
                        chaperone0 = get_full_chaperone0(
                            get_full_chaperone(chaperone), cemail
                        )
                        lenx = get_len(chaperone0)
                        if lenx > chaperone_lenx:
                            chaperone_lenx = lenx

            for i, (
                student_name,
                scores_m1_img_fpath,
                scores_img_fpath,
            ) in enumerate(scores_img_fpaths):
                chaperones_emails = self.get_chaperones_emails(student_name)
                if not chaperones_emails:
                    print_warning(
                        f"[{i+1:>{scores_img_fpaths_len2}}] "
                        + _(
                            "There is no emails of "
                            + "chaperones for {0}. Skip."
                        )
                    )
                    continue

                student_name0 = (
                    student_name[0] + "  " + student_name[1]
                    if (
                        all([is_zh_CN_char(c) for c in student_name])
                        and len(student_name) == 2
                    )
                    else student_name
                )
                student_name_len_diff = (
                    student_names_lenx
                    - get_zh_CN_chars_len(student_name0)
                    - len(student_name0)
                )
                student_name0 = " " * student_name_len_diff + student_name0

                for chaperone, cemails in chaperones_emails:
                    for cemail in cemails:
                        chaperone = get_full_chaperone(chaperone)
                        sender = (
                            _("Teacher {0}")
                            if is_zh_CN
                            else (
                                _("Mr. {0}")
                                if self.teacher.is_male
                                else _("Ms. {0}")
                            )
                        ).format(self.teacher.name)
                        chaperone0 = get_full_chaperone0(chaperone, cemail)
                        chaperone_len_diff = (
                            chaperone_lenx
                            - get_zh_CN_chars_len(chaperone0)
                            - len(chaperone0)
                        )

                        self.email.send(
                            subject=msg_subject,
                            receivers=[cemail],
                            html=self.html,
                            body_images={
                                "scores_img": scores_m1_img_fpath,
                                "scores_m1_img": scores_img_fpath,
                            },
                            body_params={
                                "chaperone": chaperone,
                                "scores_s": _(
                                    'The "{0}" scores of {1} are: '
                                ).format(self.score.full_name, student_name),
                                "sender": sender,
                            },
                        )

                        print_info(
                            f"[{i+1:>{scores_img_fpaths_len2}}/{scores_img_fpaths_len}] "
                            + _(
                                'The scores information of "{0}" has been '
                                + "sent to {2}{1}"
                            ).format(
                                student_name0,
                                chaperone0,
                                " " * chaperone_len_diff,
                            )
                        )

    @property
    def wb(self):
        if not self._wb:
            self._wb = load_workbook(self.fpath)
        return self._wb

    @property
    def sheet0(self):
        wb = self.wb
        if not self._sheet0:
            self._sheet0 = wb[wb.sheetnames[0]]
        return self._sheet0

    @property
    def teacher(self):
        if not self._teacher:
            self._teacher = self.score.teacher
        return self._teacher

    def get_chaperones_emails(self, student_name):
        emails = []
        student_name = student_name
        sheet = self.sheet0
        for col_i in range(2, sheet.max_column + 1):
            if sheet.cell(1, col_i).value == student_name:
                for row_i in range(2, sheet.max_row + 1):
                    cemails = sheet.cell(row_i, col_i).value
                    if cemails:
                        chaperone = sheet.cell(row_i, 1).value
                        cemails = (
                            cemails.replace("/", " ")
                            .replace("、", " ")
                            .replace("|", " ")
                            .replace(";", " ")
                            .replace("：", " ")
                            .replace("\n", " ")
                            .strip()
                            .split(" ")
                        )
                        emails.append([chaperone, cemails])

        if not emails:
            return None

        return emails

    @property
    def fpath(self):
        if not self._fpath:
            fpath = self.score.sclass_dpath / (
                _("parental_emails") + self.fext0
            )
            if not fpath.exists():
                fpath0 = parental_emails_fpath0
                shutil.copy(fpath0, fpath)
                print_warning(
                    _(
                        'Parental emails spreadsheet "{0}"'
                        + ' doesn\'t exist, spreadsheet "{1}"'
                        + ' was copied to "{0}".'
                    ).format(fpath, fpath0)
                )
                wb = load_workbook(fpath)
                sheet = wb[wb.sheetnames[0]]
                for i, sname in enumerate(self.score.student_names):
                    sheet.cell(1, 2 + i, sname)

                chaperone_row_offset = 2
                for i, chaperone in enumerate(self.chaperones):
                    sheet.cell(i + chaperone_row_offset, 1, chaperone)
                wb.save(fpath)

                print_info(
                    _(
                        "The student's name has been filled "
                        + 'in spreadsheet "{0}".'
                        + " Please fill in the email "
                        + "addresses according to the "
                        + "comments. (Ok! open the file for "
                        + "me. [Press any key to open it])"
                    ).format(fpath)
                )
                input0()
                open_path(fpath)
                print_info(
                    _(
                        "(Ok! I have filled them in? [Press any key to continue])"
                    )
                )
                input0()

            self._fpath = fpath

        return self._fpath


# The end.
