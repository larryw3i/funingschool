import getopt
import sys
import argparse

from helper.trans import _


def get_subparser(assistant):
    subparsers = assistant.subparsers
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

    args = assistant.parser.parse_args()

    if not args.command:
        assistant.parser.print_help()
        return

    if args.command == "docs":
        if args.generate:
            from helper.docs.write_doc import write

            lang = args.locale
            write(lang)
            pass
        else:
            get_subparser(assistant).print_help()
            pass

    pass


# The end.
