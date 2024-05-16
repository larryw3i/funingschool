import os
import sys
from pathlib import Path
import tomllib
import re
import argparse
import subprocess
from datetime import datetime

project_path = Path(__file__).parent.parent
pyproject_toml_path = project_path / "pyproject.toml"
pyvenv_path = project_path / "venv"
src_path = project_path / "src"
app_name = "fnschool"
fnschool_path = src_path / app_name
locale_dir = fnschool_path / "locales"
pot_path = locale_dir / "fnschool.pot"
lc_messages_path = locale_dir / "en_US" / "LC_MESSAGES"
mo0_path = lc_messages_path / (app_name + ".mo")
po0_path = lc_messages_path / (app_name + ".po")
sha256es_fpath = project_path / "releases" / "SHA256es"
dist_dpath = project_path / "dist"
dists_fpath = dist_dpath / "*"

is_win = sys.platform.startswith("win")

pyvenv_activate_path = (
    (pyvenv_path / "Scripts" / "activate" ).as_posix() if is_win else
    (pyvenv_path / "bin" / "activate").as_posix() 
)
def run_sh(sh_txt=""):
    return os.system(sh_txt)


def run_sh_venv(sh_txt=""):
    sh_txt = get_activate_cmd() + sh_txt
    return os.system(sh_txt)


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

    cmd = ""
    cmd += "pip3 install -U " + deps
    print(cmd.replace(";", "\n"))
    run_sh_venv(cmd)
    print("Dependencies was installed.")


def update_message():
    run_sh_venv(
        f"pybabel extract {fnschool_path} -o {pot_path};"
        + f"pybabel update -i {pot_path} -d {locale_dir} -D {app_name}"
    )


def compile_message():
    run_sh_venv(f"pybabel compile -d {locale_dir} -D {app_name}")


def add_message(language_code):
    run_sh_venv(
        f"pybabel init -d {locale_dir} -l {language_code} "
        + f"-i {pot_path} -D {app_name}"
    )


def update_version():
    version_p = r'__version__ = ["|\'][0-9]{8}.[0-9]{4}.[0-9]{2}["|\']'
    _date = datetime.now()
    version = _date.strftime("%Y%m%d.%H%M.%S")
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


def get_dists_hash():
    _sh = "cd dist; sha256sum *; cd ..;"
    _hash = subprocess.check_output(_sh, shell=True, universal_newlines=True)
    return _hash


def build(args):
    _sh = ";".join(
        [
            "python3 scripts/housekeeper.py message C",
            "python3 scripts/housekeeper.py version -u",
            f"rm -rf {dists_fpath}",
            "python3 -m build",
        ]
    )
    print(_sh)
    run_sh_venv(_sh)
    if args.twine:
        _sh = f"python3 -m twine upload {dists_fpath}"
        run_sh_venv(_sh)
        sha256_txt = None
        with open(sha256es_fpath, "r") as f:
            sha256_txt = f.read()
        _hash = get_dists_hash()
        print(_hash)
        sha256_txt = _hash + sha256_txt
        with open(sha256es_fpath, "w+") as f:
            f.write(sha256_txt)
        print(f"SHA256 hash of '{dists_fpath}'  was saved.")


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
    action="store_true",
    help="Update version of {app_name} automatically.",
)
parser_version.set_defaults(func=set_version)

parser_build = subparsers.add_parser(
    "build", help=f"Build {app_name} sources."
)
parser_build.add_argument(
    "-t", "--twine", default=False, action="store_true", help="Upload to PYPI."
)
parser_build.set_defaults(func=build)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()

# The end.
