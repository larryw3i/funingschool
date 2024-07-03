
import shutil
from fnschool import *
from fnschool.exam import *
from fnschool.exam.path import *

class FnEmail():
    def __init__(self,score=None):
        self._fpath = None
        self._score = score
        self._teacher = None
        self.fext0=".xlsx"
        self._wb = None
        self._sheet0 = None
        pass

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

    @property
    def scores(self):
        if not self._scores:
            from fnschool.exam import Score as FnScore
            self._score = FnScore()
        return self._score

    def get_emails(self,student_name):
        emails = []
        student_name = student_name
        sheet = self.sheet0
        for col_i in range(2,sheet.max_column+1):
            if sheet.cell(1,col_i).value == student_name:
                for row_i in range(2,sheet.max_row+1):
                    cemails = sheet.cell(row_i,col_i).value
                    if cemails:
                        chaperones = sheet.cell(row_i,1).value
                        cemails = (
                            cemails
                            .split("/")
                            .split("、")
                            .split("|")
                            .split(";")
                            .split("：")
                            .split("\n")
                        )
                        emails.append([chaperones,cemails])


        if not emails:
            return None
        return emails


    @property
    def fpath(self):
        if not self._fpath:
            fpath = self.score.sclass_dpath/(_("parental_emails")+self.fext0)
            if not fpath.exists():
                fpath0 = fpath0 
                shutil.copy(fpath0,fpath)
                print_warning(
                    _(
                        "Parental emails spreadsheet \"{0}\""
                        + " doesn't exist, spreadsheet \"{1}\""
                        + " was copied to \"{0}\"."
                    )
                )
                wb = load_workbook(fpath)
                sheet = wb[wb.sheetnames[0]]
                for i,sname in enumerate(self.score.student_names):
                    for col_i in range(2,sheet.max_column+1):
                        sheet.cell(1,col_i,sname)
                wb.save(fpath)

                print_info(
                    _(
                        "The student's name has been filled "
                        + "in spreadsheet \"{0}\"."
                        + " Please fill in the email "
                        + "addresses according to the "
                        + "comments. (Ok! open the file for "
                        + "me. [Press any key to open it])"

                    )
                )
                input0()

                print_info(
                    _(
                        "(Ok! I have filled them in? [Press any key to continue])"
                    )
                ) 
                input0()

            self._fpath = fpath

        return self._fpath

# The end.
