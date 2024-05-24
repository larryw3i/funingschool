import os
import sys

from fnschool import *
from fnschool.canteen.entry import *
from fnschool.exam.entry import *


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

    parse_canteen(subparsers)
    parse_exam(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


# The end.
