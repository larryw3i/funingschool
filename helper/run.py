
import getopt
import sys
import argparse

import argparse
from helper.trans import _

def get_parser():
    parser = argparse.ArgumentParser(description=_('Helper for funingschool project.'))
    docs_subparsers = parser.add_subparsers(dest='docs', help=_('commands for documents.'))
    
    docs_gen_parser = docs_subparsers.add_parser('generate', help=_('Generate documents.'))
    docs_gen_parser.add_argument('-l', '--locale', required=False,
                              help=_('The specified local language for generating document.'))
   
    return parser

def  start():
    parser = get_parser()
    args = parser.parse_args()
    
    if not args.docs:
        parser.print_help()
        return
    
    if args.docs == 'generate':
        if args.generate:
            pass

# The end.
