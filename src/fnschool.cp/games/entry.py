import os
import sys
from fnschool import *


def set_games(args):
    from fnschool.games.start import Start

    print_app()

    game_start = Start()
    if args.action in "start":
        game_start.run()

    else:
        print_info(_("Function is not found."))


def parse_games(subparsers):
    parser_games = subparsers.add_parser(
        "games", help=_("Game related functions.")
    )
    parser_games.add_argument(
        "action",
        choices=[
            "start",
        ],
        help=_('The functions of game. "start": Start games module. '),
    )
    parser_games.set_defaults(func=set_games)


# The end.
