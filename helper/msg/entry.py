import os
import sys
from helper import *


def set_msg(args):
    from helper.msg.fnmsg import Msg

    if args.action in "update":
        msg = Msg()
        msg.update()
        pass
    elif args.action in "compile":
        msg = Msg()
        msg.compile()
        pass
    elif args.action in "add":
        msg = Msg()
        if not args.locale:
            print(
                _('The "add" function need a "locale" argument.')
            )
        msg.add(args.locale)
        pass

    else:
        print(_("Function is not found."))


def parse_msg(subparsers):
    parser = subparsers.add_parser(
        "msg", help=_("'gettext' related functions.")
    )
    parser.add_argument(
        "action",
        choices=["update", "compile", "add"],
        help=_(
            '"update": Update message catalogs.'
            + '"compile": Compile message catalogs. '
            + '"add": Add locale message catalogs.'
        ),
    )
    parser.add_argument(
        "-l",
        "--locale",
        required=False,
        help=_(
            'The locale language code for '
            + 'adding message catalogs.'
        )
    )

    parser.set_defaults(func=set_msg)


# The end.
