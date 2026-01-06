import getopt
import sys
import argparse

import argparse
from helper.trans import _


def get_subparser(subparsers):
    subparser = subparsers.add_parser("docs", help=_("Commands for documents."))
    subparser.add_argument(
        "-g", "--generate", action="store_true", help=_("Generate documents.")
    )
    subparser.add_argument(
        "-l",
        "--locale",
        help=_("The specified local language for generating document."),
    )
    return subparser


def start(assistant):

    subparser = get_subparser(assistant.subparsers)
    parser = assistant.parser
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == "docs":
        if args.generate:
            from helper.docs.generate import write

            lang = args.locale
            write(lang)
            pass
        else:
            subparser.print_help()
            pass

    pass


# The end.
