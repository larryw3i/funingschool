import os
import sys
from pathlib import Path
import tomllib
import re
import argparse
from datetime import datetime

project_path = Path(__file__).parent.parent
pyproject_toml_path = project_path / "pyproject.toml"
pyvenv_path = project_path / "venv"
pyvenv_activate_path = (pyvenv_path / "bin" / "activate").as_posix()
src_path = project_path / "src"
app_name = "fnschool"
fnschool_path = src_path / app_name
locale_dir = fnschool_path / "locales"
pot_path = locale_dir / "fnschool.pot"
lc_messages_path = locale_dir / "en_US" / "LC_MESSAGES"
mo0_path = lc_messages_path / (app_name + ".mo")
po0_path = lc_messages_path / (app_name + ".po")


def get_activate_cmd():
    cmd = ""
    if not pyvenv_path.exists():
        cmd += "python3 -m venv " + pyvenv_path.as_posix() + ";"
    cmd += f". {pyvenv_activate_path};"
    return cmd


def install_dependencies():
    project_data = None
    with open(pyproject_toml_path, "rb") as f:
        project_data = tomllib.load(f)
    deps = project_data.get("project").get("dependencies")
    deps += ["Babel"]
    deps = '"' + '" "'.join(deps) + '"'

    cmd = get_activate_cmd()
    cmd += "pip3 install -U " + deps
    print(cmd.replace(";", "\n"))
    os.system(cmd)
    print("Dependencies was installed.")


def update_message():
    os.system(
        get_activate_cmd()
        + f"pybabel extract  {fnschool_path} -o {pot_path};"
        + f"pybabel update -i {pot_path} -d {locale_dir} -D {app_name}"
    )


def compile_message():
    os.system(
        get_activate_cmd() + f"pybabel compile -d {locale_dir} -D {app_name}"
    )


def add_message(language_code):
    os.system(
        get_activate_cmd()
        + f"pybabel init -d {locale_dir} -l {language_code} "
        + f"-i {pot_path} -D {app_name}"
    )


def update_version():
    version_p = r'__version__ = ["|\'][0-9]{4}.[0-9]{4}["|\']'
    _date = datetime.now()
    version = _date.strftime("%Y.%m%d")
    init_fpath = fnschool_path / "__init__.py"
    with open(init_fpath, "r+") as f:
        content = f.read()
        content = re.sub(version_p, f'__version__ = "{version}"', content)
        f.seek(0)
        f.truncate()
        f.write(content)
    print("Version was updated.")


def print_no_args():
    print("Nothing to do.")


def set_message(args):
    args_do = args.do
    if args_do == "U":
        update_message()
    elif args_do == "C":
        compile_message()
    elif args_do == "A":
        add_message(args.local)
    else:
        print_no_args()


def set_version(args):
    if args.update:
        update_version()
    else:
        print_no_args()


def set_dependencies(args):
    if args.action == "I":
        install_dependencies()


parser = argparse.ArgumentParser(
    prog="housekeeper",
    description="Housekeeper of Funingschool.",
    epilog=f"Some functions fo {app_name} project.",
)

subparsers = parser.add_subparsers(help="The functions to run.")
parser_msg = subparsers.add_parser(
    "message", help="Gettext message related functions."
)
parser_msg.add_argument(
    "do",
    choices=["U", "A", "C"],
    help=(
        "'U' for updating messages,"
        + "'A' for adding message to specified language code,"
        + "'C' for compile messages."
    ),
)
parser_msg.add_argument(
    "-l", "--local", help="language code for adding message."
)
parser_msg.set_defaults(func=set_message)

parser_deps = subparsers.add_parser(
    "dependencies", help="Dependencies related function."
)

parser_deps.add_argument("action", help="'I' for installing all dependencies.")
parser_deps.set_defaults(func=set_dependencies)

parser_version = subparsers.add_parser(
    "version", help=f"Version related functions."
)
parser_version.add_argument(
    "-u",
    "--update",
    default=set_version,
    action="store_true",
    help="Update version of {app_name} automatically.",
)
parser_version.set_defaults(func=set_version)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()

# The end.
