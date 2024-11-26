import os
import sys
from helper import *


def set_build(args):
    from helper.packing.build import Build

    if args.action in "now":
        build = Build()
        build.build()
        pass
    elif args.action in "upload":
        build = Build()
        build.build(upload=True)
        pass
    else:
        print_info(_("Function is not found."))


def parse_build(subparsers):
    parser = subparsers.add_parser(
        "build", help=_("'build' related functions.")
    )
    parser.add_argument(
        "action",
        choices=["now", "upload"],
        help=_(
            '"now": Build "fnschool" now. '
            + '"upload": Build and upload "fnschool" via "twine".'
        ),
    )
    parser.set_defaults(func=set_build)
