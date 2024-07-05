import os
import sys

from helper import *


def set_docs(args):

    if args.action in "readme":
        pass
    else:
        print_info(_("Function is not found."))


def parse_docs(subparsers):
    parser_canteen = subparsers.add_parser(
        "docs", help=_("Documentation related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=["readme"],
        help=_('"readme": Generate README.md and README.*.md.'),
    )
    parser_canteen.set_defaults(func=set_docs)
