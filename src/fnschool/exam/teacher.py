import os
import sys
from fnschool import *
from fnschool.exam import *
from fnschool.exam.path import *


class Teacher(User):
    def __init__(
        self,
    ):
        super().__init__(user_exam_dpath, teach_name_fpath)
        self._name = None
        self._dpath = None
        self._exam_dpath = None
        pass

    @property
    def exam_dpath(self):
        if not self._exam_dpath:
            self._exam_dpath = self.dpath / _("exam")
            if not self._exam_dpath.exists():
                os.makedirs(self._exam_dpath, exist_ok=True)
            return self._exam_dpath
        return self._exam_dpath
