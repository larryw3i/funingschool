import os
import sys
from helper import *


def set_dep(args):
    from helper.dep.pkg import Pkg

    if args.action in "install":
        dep = Dep()
        dep.install()
        pass
    else:
        print_info(_("Function is not found."))


def parse_dep(subparsers):
    parser = subparsers.add_parser(
        "dep", help=_("'dependencies' related functions.")
    )
    parser.add_argument(
        "action",
        choices=["install"],
        help=_(
            '"install": Install all dependencies ' + "in virtual environment."
        ),
    )
    parser.set_defaults(func=set_dep)


# The end.
