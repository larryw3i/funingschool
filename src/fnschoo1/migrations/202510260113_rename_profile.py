import os
import sqlite3
import sys
from pathlib import Path

SRC_PATH = Path(__file__).parent.parent.parent
if not SRC_PATH in sys.path:
    sys.path.insert(0, SRC_PATH.as_posix())

from fnschoo1.migrations import *


def migrate():
    conn1 = sqlite3.connect(db_path)
    tables1 = conn1.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
    ).fetchall()
    tables1 = [t[0] for t in tables1]
    print(tables1)
    if not any(["profiles" in name for name in tables1]):
        return


if __name__ == "__main__":
    migrate()

# The end.
