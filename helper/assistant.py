import getopt
import sys
import argparse
from pathlib import Path
import importlib

import argparse
from helper.trans import _

helper_dir = Path(__file__).parent
project_dir = helper_dir.parent


class Assistant:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog=_("python -m helper"),
            description=_("Helper for funingschool project."),
        )
        self.subparsers = self.parser.add_subparsers(
            dest="command", help=_("commands.")
        )
        self.helper_dir = helper_dir
        self.project_dir = project_dir

    def start(self):
        dirs = [d for d in self.helper_dir.iterdir() if d.is_dir()]
        dirs_cp = []
        for p in dirs:
            path_names = [p.name for p in p.iterdir()]
            if "__init__.py" in path_names and "run.py" in path_names:
                dirs_cp.append(p)

        dirs = dirs_cp
        for p in dirs:
            module = module = importlib.import_module(f"helper.{p.name}.run")
            if hasattr(module, "start"):
                start_func = getattr(module, "start")
                if callable(start_func):
                    start_func(self)


# The end.
