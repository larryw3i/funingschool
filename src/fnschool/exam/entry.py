import os
import sys
from fnschool import *


def set_exam(args):
    from fnschool.exam.score import Score

    print_app()

    if args.action in "enter":
        score = Score()
        score.enter()
    elif args.action in "read":
        score = Score()
        score.read()
    else:
        print_info(_("Function is not found."))


def parse_exam(subparsers):
    parser_canteen = subparsers.add_parser(
        "exam", help=_("Examination related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=["enter", "read"],
        help=_(
            '"enter": Enter the examination scores. '
            + '"read":Read the examination scores.'
        ),
    )
    parser_canteen.set_defaults(func=set_exam)


# The end.
