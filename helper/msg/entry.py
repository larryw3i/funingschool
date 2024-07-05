import os
import sys
from helper import *


def set_msg(args):
    from helper.msg.fnmsg import Msg

    if args.action in "updte":
        msg = Msg()
        msg.update()
        pass
    elif args.action in "compile":
        msg = Msg()
        msg.compile()
        pass
    else:
        print_info(_("Function is not found."))


def parse_msg(subparsers):
    parser_canteen = subparsers.add_parser(
        "msg", help=_("'gettext' related functions.")
    )
    parser_canteen.add_argument(
        "action",
        choices=["update", "compile"],
        help=_(
            '"update": Update message catalogs.'
            + '"compile": Compile message catalogs.'
        ),
    )
    parser_canteen.set_defaults(func=set_msg)


# The end.
