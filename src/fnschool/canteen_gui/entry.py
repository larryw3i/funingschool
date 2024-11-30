import os
import sys
from fnschool import *


def set_canteen_gui(args):
    from fnschool.canteen_gui.bill import Bill

    print_app()

    bill = Bill()
    if args.action in "mk_bill":
        bill.make_spreadsheets()
        pass

    elif args.action in "merge_foodsheets":
        bill.merge_foodsheets()
        pass

    else:
        print_info(_("Function is not found."))
        pass
    pass


def parse_canteen_gui(subparsers):
    parser_canteen_gui = subparsers.add_parser(
        "canteen_gui", help=_("Canteen GUI related functions.")
    )
    parser_canteen_gui.add_argument(
        "action",
        choices=["mk_bill", "merge_foodsheets", ],
        help=_(
            'The functions of canteen. "mk_bill_gui": Make bill (via GUI). '
            + '"merge_foodsheets": Merge food sheets (via GUI).'
        ),
    )
    parser_canteen_gui.set_defaults(func=set_canteen_gui)

# The end.
