import os
import sys
import uuid
from pathlib import Path

FNSCHOO1_PATH = Path(__file__).parent.parent
db_path = FNSCHOO1_PATH / "db.sqlite3"
db_cp_path = FNSCHOO1_PATH / "db.cp"

if not db_cp_path.exists():
    os.makedirs(db_cp_path, exist_ok=False)


def new_uuid_db_path():
    uuid_db_path = db_cp_path / ("db." + str(uuid.uuid4()) + ".sqlite3")
    return uuid_db_path


# The end.
