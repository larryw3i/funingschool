#!./venv/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from pathlib import Path

sys.path.append((Path(__file__).parent / "src").as_posix())

from fnschool import show_gui

if __name__ == "__main__":
    sys.argv[0] = re.sub(r"(-script\.pyw|\.exe)?$", "", sys.argv[0])
    sys.exit(show_gui())
