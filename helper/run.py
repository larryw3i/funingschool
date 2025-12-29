
import getopt
import sys
import argparse

import argparse
from helper.trans import _

def get_parser():
    return parser

def  start():
    from helper.docs.run import start as docs_start

    parser = argparse.ArgumentParser(prog=_("python -m helper"),description=_('Helper for funingschool project.'))
    subparsers = parser.add_subparsers(dest='command', help=_('commands.'))

    docs_start(parser,subparsers)

# The end.
