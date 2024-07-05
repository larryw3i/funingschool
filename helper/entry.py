import os
import sys

from helper import *

from helper.msg.entry import parse_msg
from helper.build.entry import parse_build
from helper.readme.entry import parse_readme

sys.path.append((Path(__file__).parent.parent).as_posix())


def read_cli():
    parser = argparse.ArgumentParser(
        prog=_("Helper of fnschool project"),
        description=_("Command line interface of fnschool project tools."),
        epilog=_("Enj0y it."),
    )
    subparsers = parser.add_subparsers(help=_("The tools to run."))

    parse_msg(subparsers)
    parse_build(subparsers)
    parse_readme(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


# The end.
