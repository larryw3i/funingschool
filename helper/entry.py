import importlib
import inspect
import os
import sys

from helper import *
from helper.dep.entry import parse_dep
from helper.docs.entry import parse_docs
from helper.msg.entry import parse_msg
from helper.packing.entry import parse_build

p_dpath = (Path(__file__).parent.parent).as_posix()
if not p_dpath in sys.path:
    sys.path.append(p_dpath)


module_dpath = Path(__file__).parent
entry_name = "entry.py"


def get_entries():
    entries = [
        ".".join(
            os.path.splitext(p.relative_to(module_dpath.parent))[0]
            .replace("\\", "/")
            .split("/")
        )
        for p in module_dpath.glob(f"*/{entry_name}")
    ]
    return entries


def read_cli():
    parser = argparse.ArgumentParser(
        prog=_("Helper of fnschool project"),
        description=_("Command line interface of fnschool project tools."),
        epilog=_("Enj0y 1t."),
    )
    subparsers = parser.add_subparsers(help=_("The tools to run."))
    entries = get_entries()

    for entry in entries:
        entry = importlib.import_module(entry)
        names = dir(entry)
        for name in names:
            attr = getattr(entry, name)
            if inspect.isfunction(attr):
                if name.startswith("parse_"):
                    attr(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


# The end.
