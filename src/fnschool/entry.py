import os
import sys

from fnschool import *


def set_canteen(args):
    from fnschool.canteen.bill import Bill

    bill = Bill()
    if args.action in "mk_tspreadsheet":
        bill.make_spreadsheets()
    elif args.action in "help_friends":
        bill.help_friends_via_email()

    else:
        print_info(_("Function is not found."))


def show_gui():
    print_info("Just wait.")
    pass


def read_cli():
    parser = argparse.ArgumentParser(
        prog=_("fnschool"),
        description=_("Command line interface of fnschool."),
        epilog=_("Enjoy it."),
    )
    subparsers = parser.add_subparsers(help=_("The modules to run."))
    parser_canteen = subparsers.add_parser(
        "canteen", help=_("Canteen related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=["mk_tspreadsheet", "help_friends"],
        help=_("The functions of canteen."),
    )
    parser_canteen.set_defaults(func=set_canteen)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


# The end.
