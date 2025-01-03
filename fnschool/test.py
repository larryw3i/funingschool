import os
import sys
from pathlib import Path
import unittest

sys.path.append(Path(__file__).parent.parent.as_posix())

from fnschool import *


class TestCateen(unittest.TestCase):
    def test_open_file_via_sys_app(self):
        open_file_via_sys_app(
            file_path=Path(
                Path(__file__).parent.parent.parent
                / "tests"
                / "files"
                / "changsheng.3.1-3.15.xlsx"
            ).as_posix()
        )


if __name__ == "__main__":
    unittest.main()
