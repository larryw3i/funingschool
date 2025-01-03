import os
import sys
from fnschool import *

exam_dpath = Path(__file__).parent
exam_data_dpath = exam_dpath / "data"
user_exam_dpath = user_data_dir / _("exam")
teach_name_fpath = user_exam_dpath / (_("teacher_name") + ".txt")
score_fpath0 = exam_data_dpath / "score.xlsx"
parental_emails_fpath0 = exam_data_dpath / "parental_emails.xlsx"

for d in [
    user_exam_dpath,
]:
    if not d.exists():
        os.makedirs(d.as_posix(), exist_ok=True)

if not teach_name_fpath.exists():
    if not teach_name_fpath.parent.exists():
        os.makedirs(teach_name_fpath.parent.as_posix(), exist_ok=True)
    with open(teach_name_fpath, "w", encoding="utf-8") as f:
        f.write("")

# The end.
