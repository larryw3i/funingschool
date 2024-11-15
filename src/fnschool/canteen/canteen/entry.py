import os
import sys
from fnschool import *


def set_canteen(args):
    from fnschool.canteen.bill import Bill

    print_app()

    bill = Bill()
    if args.action in "mk_bill":
        bill.make_spreadsheets()

    elif args.action in "merge_foodsheets":
        bill.merge_foodsheets()

    else:
        print_info(_("Function is not found."))


def parse_canteen(subparsers):
    parser_canteen = subparsers.add_parser(
        "canteen", help=_("Canteen related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=["mk_bill", "merge_foodsheets"],
        help=_(
            'The functions of canteen. "mk_bill": Make bill. '
            + '"merge_foodsheets": Merge food sheets.'
        ),
    )
    parser_canteen.set_defaults(func=set_canteen)
