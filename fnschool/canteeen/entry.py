import os
import sys
from fnschool import *


def set_canteeen(args):
    if args.action in "mk_bill":
        pass

    elif args.action in "merge_foodsheets":
        pass

    else:
        pass


def parse_canteeen(subparsers):
    parser_canteeen = subparsers.add_parser(
        "canteeen", help=_("Canteen related functions.")
    )
    parser_canteeen.add_argument(
        "action",
        choices=["mk_bill", "merge_foodsheets", ],
        help=_(
            'The functions of canteen. "mk_bill": Make bill. '
            + '"merge_foodsheets": Merge food sheets.'
        ),
    )
    parser_canteeen.set_defaults(func=set_canteeen)

# The end.
