import os
import sys
from fnschool import *


def set_exam(args):
    from fnschool.exam.score import FnScore

    print_app()

    score = FnScore()
    if args.action in "enter_score":
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
        help=_("The functions of examination."),
    )
    parser_canteen.set_defaults(func=set_exam)
