import os
import sys
from pathlib import Path


p_dpath = (Path(__file__).parent.parent).as_posix()
if not p_dpath in sys.path:
    sys.path.append(p_dpath)


from fnschool import *
from fnschool.entry import *

read_cli()

# The end.
