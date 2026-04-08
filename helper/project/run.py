import getopt
import sys
import argparse
import tomllib
import os


import argparse
from helper.trans import _

from helper.project import pyproject_toml_path


def get_subparser(assistant):
    subparsers = assistant.subparsers
    subparser = subparsers.add_parser(
        "project", help=_("Commands for project.")
    )
    subparser.add_argument(
        "-d",
        "--dependencies",
        action="store_true",
        help=_("Print Python3 dependencies."),
    )
    subparser.add_argument(
        "-i",
        "--install",
        action="store_true",
        help=_("Install dependencies for this project."),
    )
    return subparser


def start(assistant):

    args = assistant.parser.parse_args()

    if not args.command:
        assistant.parser.print_help()
        return

    if args.command == "project":
        if args.dependencies:
            pyproject_toml = None
            with open(pyproject_toml_path, "rb") as f:
                pyproject_toml = tomllib.load(f)

            dependencies = []
            if (
                "project" in pyproject_toml
                and "dependencies" in pyproject_toml["project"]
            ):
                for dep in pyproject_toml["project"]["dependencies"]:
                    dependencies.append(dep)

            dependencies_str = " ".join([f'"{d}"' for d in dependencies])
            print(
                _("Python3 dependencies of this project: {0}").format(
                    dependencies_str
                )
            )
            if dependencies and args.install:
                os.system("python -m pip install " + dependencies_str)
            pass
        else:
            get_subparser(assistant).print_help()
            pass

    pass


# The end.
