import os
import sys
from fnschool import *


def set_canteen(args):
    from fnschool.canteen.bill import Bill

    print_app()

    bill = Bill()
    if args.action in "mk_bill":
        bill.make_spreadsheets()

    else:
        print_info(_("Function is not found."))


def parse_canteen(subparsers):
    parser_canteen = subparsers.add_parser(
        "canteen", help=_("Canteen related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=[
            "mk_bill",
        ],
        help=_("The functions of canteen."),
    )
    parser_canteen.set_defaults(func=set_canteen)
