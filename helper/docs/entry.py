import os
import sys

from helper import *


def set_docs(args):

    if args.action in "readme":
        from helper.docs.readme.content import Content

        content = Content()
        content.update()
        pass
    else:
        print_info(_("Function is not found."))


def parse_docs(subparsers):
    parser = subparsers.add_parser(
        "docs", help=_("Documentation related functions.")
    )
    parser.add_argument(
        "action",
        choices=["readme"],
        help=_('"readme": "README" files related functions.'),
    )
    parser.set_defaults(func=set_docs)
