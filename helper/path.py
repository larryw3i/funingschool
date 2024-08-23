import os
import sys
from pathlib import Path

helper_dpath = Path(__file__).parent
project_dpath = helper_dpath.parent
readme0_fpath = project_dpath / "README.html"
readme_dpath = project_dpath / "Documentation" / "README" 
dist_dpath = project_dpath / "dist"
dist_fpaths = dist_dpath / "*"
sha256es_fpath = project_dpath / "releases" / "SHA256es"
project_toml_fpath = project_dpath / "pyproject.toml"
venv_dpath = project_dpath / "venv"

src_dpath = project_dpath / "src"

# The end.
