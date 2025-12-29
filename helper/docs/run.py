
import getopt
import sys
import argparse

import argparse
from helper.trans import _


def get_subparser(subparsers):
    subparser = subparsers.add_parser('docs', help=_('Commands for documents.'))
    subparser.add_argument('-g', '--generate', required=False,
                              help=_('Generate documents.'))
    subparser.add_argument('-l', '--locale', required=False,
                              help=_('The specified local language for generating document.'))
    return subparser

def start(parser,subparsers):
    subparser = get_subparser(subparsers)
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'docs':
        if args.generate:
            pass
        else:
            subparser.print_help()
            pass


    pass

# The end.
