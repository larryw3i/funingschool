
import os
import sys
from pathlib import Path

helper_dpath = Path(__file__).parent
project_dpath = helper_dpath.parent
project_toml_fpath = project_dpath / "pyproject.toml"
venv_dpath = project_dpath / "venv"

fnschool_dpath = project_dpath / "src" / "fnschool"

# The end.
