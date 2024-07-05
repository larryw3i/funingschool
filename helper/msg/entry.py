import os
import sys
from fnschool import *


def set_msg(args):

    if args.action in "updte":
        pass
    elif args.action in "compile":
        pass
    else:
        print_info(_("Function is not found."))


def parse_msg(subparsers):
    parser_canteen = subparsers.add_parser(
        "msg", help=_("'gettext' related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=["update", "compile"],
        help=_(
            '"update": Update message catalogs.'
            + '"compile": Compile message catalogs.'
        ),
    )
    parser_canteen.set_defaults(func=set_msg)
