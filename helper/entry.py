import os
import sys

from helper import *

from helper.msg.entry import parse_msg
from helper.build.entry import parse_build
from helper.docs.entry import parse_docs
from helper.dep.entry import parse_dep

p_dpath = (Path(__file__).parent.parent).as_posix()
if not p_dpath in sys.path:
    sys.path.append(p_dpath)


def read_cli():
    parser = argparse.ArgumentParser(
        prog=_("Helper of fnschool project"),
        description=_("Command line interface of fnschool project tools."),
        epilog=_("Enj0y 1t."),
    )
    subparsers = parser.add_subparsers(help=_("The tools to run."))

    parse_msg(subparsers)
    parse_build(subparsers)
    parse_docs(subparsers)
    parse_dep(subparsers)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


# The end.
