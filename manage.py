#!/bin/python3
import sys
from pathlib import Path

project_dir = Path(__file__).parent
fnschoo1_dir = project_dir / "src"


if not fnschoo1_dir.as_posix() in sys.path:
    sys.path.insert(0, fnschoo1_dir.as_posix())

from fnschoo1.manage import main

if __name__ == "__main__":
    if sys.argv[0].endswith(".exe"):
        sys.argv[0] = sys.argv[0][:-4]
    sys.exit(main())
