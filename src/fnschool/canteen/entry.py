import os
import sys
from fnschool import *


def set_canteen(args):

    print_app()

    if args.action in "mk_bill":
        pass

    elif args.action in "merge_foodsheets":
        pass

    elif args.action in "gen_daybook":
        from fnschool.canteen.daybook.note import Note

        note = Note()
        note.gen()

    elif args.action in "ledger":
        from fnschool.canteen.ledger.daybook import Daybook

        daybook = Daybook()
        daybook.show()

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
            "merge_foodsheets",
            "gen_daybook",
            "ledger",
        ],
        help=_(
            'The functions of canteen. "mk_bill": Make bill. '
            + '"merge_foodsheets": Merge food sheets. '
            + '"ledger": Manage Ledgers.'
        ),
    )
    parser_canteen.set_defaults(func=set_canteen)


# The end.
