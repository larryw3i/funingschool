
import os
import sys
from pathlib import Path
import gettext
from helper.trans import _

from helper.assistant import helper_dir

project_dir = helper_dir.parent
locale_dir = helper_dir / "locale"
project_doc_dir = project_dir / "Documentation"
project_readme_dir = project_doc_dir / "README"
project_readme_path = project_dir / "README.md"

__cp = _

def write_readme(lang,_t):
    _ = _t
    l = lang
    readme = [
'<hr/>',
'<div align="center">',
'   <pre>',
r' _____ _   _ ____   ____ _   _  ___   ___  _     ',
r'|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    ',
r'| |_  |  \| \___ \| |   | |_| | | | | | | | |    ',
r'|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ ',
r'|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|',
'    </pre>',
'</div>',
'<p align="center">',
_('    funingschool'),
'</p>',
'',
'<h4 align="center">',
_('    NO Just some simple scripts for warehousing and consuming.'),
'</h4>',
'<hr/>',
'<p align="center">',
'    <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/README/zh_CN.md">\u7b80\u4f53\u4e2d\u6587</a> •',
'    <a href="https://github.com/larryw3i/funingschool/blob/master/README.md">English</a>',
'</p>',
'',
'<p align="center">',
'    <a href="#key-features">',
_('         Key Features'),
'    </a>',
'    •',
'    <a href="#how-to-use">',
_('         How To Use'),
'    </a>',
'    •',
'    <a href="#credits">',
_('         Credits'),
'    </a>',
'    •',
'    <a href="#support">',
_('         Support'),
'    </a>',
'    •',
'    <a href="#license">',
_('         License'),
'    </a>',
'</p>',
'',
_('![Screenshot](https://raw.githubusercontent.com/larryw3i/funingschool/master/Documentation/images/44e58998-da32-11f0-b726-700894a38a35.png)'),
'<h2 id="key-features">',
_('    Key Features'),
'</h2>',
'<h3>',
_('    warehousing and consuming'),
'</h3>',
'',
_('* Read food spreadsheets automatically.'),
_('* The simplest and most straightforward `consuming sheets`.'),
_('* Update sheets (warehousing, consuming, summing, etc) automatically.'),
_('* Reduce calculation errors.'),
_('* Effectively eliminate unit prices containing infinite decimals.'),
_('* Merge food sheets between spreadsheets.  '),
_('* Easy to use.'),
'<h2 id="how-to-use">',
_("    How To Use"),
'</h2>',
'<h3>',
_('    Install Python3'),
'</h3>',
'',
'<p>',
"",
_('on `Debian|Ubuntu`:'),
'```bash',
'sudo apt-get install python3 python3-pip python-is-python3',
'```  ',
_('For `Windows 10` and `Windows 11`, you can install Python3 from https://www.python.org/getit/ . (`fnschool` requires Python 3.12 or later)'),
'</p>',
'',
'<h3>',
_('    Install fnschool and run it'),
'</h3>',
'',
'<p>',
'',
_('Run the command line application:'),
'* `Debian|Ubuntu`: `Ctrl+Alt+T`.',
'* `Windows`: "`Win+R, powershell, Enter`".',
_("Enter the following commands:"),
'',
'</p>',
'',
'```bash',
_('# Install or update "fnschool".'),
  _("#      You may use the virtual enviroment on Debian|Ubuntu, the commands:"),
  _("#      python -m venv --system-site-packages ~/pyvenv; # Create virtual enviroment."),
  _("#      . ~/pyvenv/bin/activate; # Use it."),
'pip install -U fnschool',
_('# Update database.'),
'python -m fnschoo1.manage migrate',
_('# Start fnschoo1.'),
'python -m fnschoo1.manage',
'```',
'<h2 id="credits">',
    _("Credits"),
'</h2>',
'<p>',
"", 
_(' This software uses the following open source packages:'),
'   <ul>',
'       <li><a href="https://pandas.pydata.org/">pandas</a></li>',
'       <li><a href="https://numpy.org/">numpy</a></li>',
'       <li><a href="https://openpyxl.readthedocs.io/">openpyxl</a></li>',
'       <li><a href="https://github.com/tox-dev/platformdirs">platformdirs</a></li>',
'       <li><a href="https://matplotlib.org/">matplotlib</a></li>',
'   </ul>',
'</p>',
'',
'<h2 id="support">',
_(" Support"),
'</h2>',
'<h3>',
_(" Buy me a `coffee`:"),
'</h3>',
'',
_('![Buy me a "coffee".](https://raw.githubusercontent.com/larryw3i/funingschool/master/Documentation/images/9237879a-f8d5-11ee-8411-23057db0a773.jpeg)'),
'<h2 id="license">',
_(" License"),
'</h2>',
'<a href="https://github.com/larryw3i/funingschool/blob/master/LICENSE">',
_(" GNU LESSER GENERAL PUBLIC LICENSE Version 3"),
"</a>",
    ]
    readme = "\n".join(readme)

    file_path = project_readme_dir / (l +".md")
    if not file_path.exists():
        file_path.touch()
        print(f'"{file_path}"',_("has been created."))

    with open(file_path, 'w', encoding="UTF-8") as file:
        file.write(readme)
        print(f'"{file_path}"',_("has been updated."))

    if l == "en_US":
        if not project_readme_path.exists():
            project_readme_path.touch()
            print(f'"{project_readme_path}"',_("has been created."))
        with open(project_readme_path, 'w', encoding="UTF-8") as file:
            file.write(readme)
            print(f'"{project_readme_path}"',_("has been updated."))


def write(lang=None):
    langs = [lang] if lang else[p.name for p in locale_dir.iterdir() if p.is_dir()]

    localedir = locale_dir
    localedir = localedir.as_posix()

    for l in langs:
        mo_file=locale_dir / l / "LC_MESSAGES" / "helper.mo"
        if mo_file.exists():
            t = gettext.translation('helper', localedir, languages=[l], fallback=True)

            write_readme(l,t.gettext)

_ = __cp

# The end.
