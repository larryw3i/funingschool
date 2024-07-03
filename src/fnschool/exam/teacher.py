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
        self._scores_html_fpath = None
        pass

    @property
    def exam_dpath(self):
        if not self._exam_dpath:
            self._exam_dpath = self.dpath / _("exam")
            if not self._exam_dpath.exists():
                os.makedirs(self._exam_dpath, exist_ok=True)
            return self._exam_dpath
        return self._exam_dpath

    @property
    def scores_html_fpath(self):
        if not self._scores_html_fpath:
            fpath = self.exam_dpath / (_("scores_info") + ".html")
            if not fpath.exists():
                with open(fpath, "w+", encoding="utf-8") as f:
                    f.write(
                        "\n".join(
                            [
                                "<h1>" + _("Hello!") + " {{ chaperone }}:</h1>",
                                "<p>{{ scores_s }}</p>",
                                '<img src="{{ scores_m1_img.src }}" width=100%>',
                                '<img src="{{ scores_img.src }}" width=100%>',
                                "<p>",
                                "   " + _("Kind regards!"),
                                "</p>",
                                '<p style="text-align: right;">',
                                "   {{ sender }}",
                                "</p>",
                            ]
                        )
                    )
            self._scores_html_fpath = fpath
        return self._scores_html_fpath


# The end.
