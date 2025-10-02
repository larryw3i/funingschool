import os
import sys

from fnschool import *


def set_class(args):

    print_app()

    if args.action in "set_bell":
        pass

    else:
        print_info(_("Function is not found."))


def parse_class(subparsers):
    parser_class = subparsers.add_parser(
        "class", help=_("Class related functions.")
    )
    parser_class.add_argument(
        "action",
        choices=[
            "set_bell",
        ],
        help=_('The functions of class. "set_bell": Configurate bell. '),
    )
    parser_class.set_defaults(func=set_class)


# The end.
