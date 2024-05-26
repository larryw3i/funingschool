import os
import sys
from fnschool import *


def set_exam(args):
    from fnschool.exam.score import Score

    print_app()

    if args.action in "enter_score":
        score = Score()
        score.enter()

    else:
        print_info(_("Function is not found."))


def parse_exam(subparsers):
    parser_canteen = subparsers.add_parser(
        "exam", help=_("Examination related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=[
            "enter_score",
        ],
        help=_("Enter the examination scores."),
    )
    parser_canteen.set_defaults(func=set_exam)
