import os
import sys
import argparse
from housekeeper import *

sys.path.append((Path(__file__).parent.parent).as_posix())


def read_cli():
    parser = argparse.ArgumentParser(
        prog=_("Housekeeper of fnschool"),
        description=_("Command line interface of school project tools."),
        epilog="(^_^)",
    )
    subparsers = parser.add_subparsers(help=_("The modules to run."))

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


# The end.
