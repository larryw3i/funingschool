import os
import sys
from fnschool import *

exam_dpath = Path(__file__).parent
user_exam_dpath = user_data_dir / _("exam")
teach_name_fpath = user_exam_dpath / (_("teacher_name") + ".txt")
