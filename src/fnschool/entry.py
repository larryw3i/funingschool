import os
import sys
import importlib
import inspect

from fnschool import *
from fnschool.canteen.entry import *
from fnschool.exam.entry import *
from fnschool.external import *


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


def show_gui():
    print_info(_("Just wait."))
    pass


def read_cli():
    parser = argparse.ArgumentParser(
        prog=_("fnschool"),
        description=_("Command line interface of fnschool."),
        epilog=_("Enjoy it."),
    )
    subparsers = parser.add_subparsers(help=_("The modules to run."))
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

    print_sponsor()


# The end.
