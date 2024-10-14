import os
import sys

from helper import *


class Content:
    def __init__(self):
        pass

    def update(self):

        lang_codes = get_language_codes()
        global _
        _cp = _
        for lc in lang_codes:
            T = gettext.translation(
                t_domain, locale_dir, fallback=True, languages=[lc]
            )
            T.install()
            t = T.gettext
            content = self.get_content(t_func=t)

            _ = _cp

            if lc == "en_US":
                with open(readme0_fpath, "w+", encoding="utf-8") as f:
                    f.write(content)
            readme_fpath = readme_dpath / f"{lc}.md"
            with open(readme_fpath, "w+", encoding="utf-8") as f:
                f.write(content)
            print(_('README file "{0}" was updated.').format(readme_fpath))

    def get_content(self, t_func=None):
        _ = t_func
        return (
            r"""
<div align="center">
  <br>
  <pre>"""
            + r"""
 _____ _   _ ____   ____ _   _  ___   ___  _     
|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    
| |_  |  \| \___ \| |   | |_| | | | | | | | |    
|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ 
|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|
"""
            + f"""
  </pre>
  <br>
  funingschool
  <br>
</div>

<h4 align="center">
    {_("NO Just some simple scripts for warehousing and consuming.")}
</h4>

<p align="center">
    <a href="https://gitee.com/larryw3i/funingschool/blob/master/\
Documentation/README/zh_CN.md">简体中文</a> •
    <a href="https://github.com/larryw3i/funingschool/blob/master/\
README.md">English</a>
</p>

<p align="center">
    <a href="#key-features">
        {_("Key Features")}
    </a>
    •
    <a href="#how-to-use">
        {_("How To Use")}
    </a>
    •
    <a href="#credits">
        {_("Credits")}
    </a>
    •
    <a href="#support">
        {_("Support")}
    </a>
    •
    <a href="#license">
        {_("License")}
    </a>
</p>

![{_("Screenshot")}]({_("https://raw.githubusercontent.com/larryw3i/funingschool/master/"+
"Documentation/images/9432e132-f8cd-11ee-8ee6-f37309efa64b.png")})

<h2 id="key-features">
    {_("Key Features")}
</h2>

<h3>
    {_("warehousing and consuming")}
</h3>

* {_("Read food spreadsheets automatically.")}
* {_("The simplest and most straightforward `consuming sheets`.")}
* {_(
    "Update sheets (warehousing, consuming, "
    +"summing, etc) automatically."
)}
* {_("Reduce calculation errors.")}
* {_("Effectively eliminate unit prices containing infinite decimals.")}
* {_("Easy to use.")}

<h3>
    {_("Test statistics")}
</h3>

* {_('An easy-to-use "test score entry form".')}
* {_(
    "Clear test results at a glance, "
    + "converting table data into Intuitive images."
)}
* {_("Display comments.")}
* {_("Effectively assist testers, especially teachers and students.")}

<h2 id="how-to-use">
    {_("How To Use")}
</h2>

<h3>
    {_("Install Python3")}
</h3>
<p>

{_("on `Ubuntu`:")}

```bash
sudo apt-get install python3 python3-pip
```  
{_(
    "For `Windows 10` and `Windows 11`, you can install Python3 from "
    + "https://www.python.org/getit/ ."
)}
</p>

<h3>
    {_("Install fnschool and run it")}
</h3>

<p>

{_(
    "Run the command line application "
    + "(`Ubuntu`: `Ctrl+Alt+T`. `Windows`: \"`Win+R, powershell, Enter`\"),"
    + " and enter the following commands:"
)}

</p>

```bash
# {_("install fnschool.")}
pip3 install -U fnschool
# {_("run `warehousing and consuming` module.")}
fnschool-cli canteen mk_bill
# { _("run `test statistics` module.")}
fnschool-cli exam enter
```

>{_("Note: "+
    "Read the information it prompts carefully, "
    + "which is the key to using it well."
)}

<h2 id="credits">
    {_("Credits")}
</h2>
<p>
    {_("This software uses the following open source packages:")}
    <ul>
        <li><a href="https://github.com/tartley/colorama">colorama</a></li>
        <li><a href="https://pandas.pydata.org/">pandas</a></li>
        <li><a href="https://numpy.org/">numpy</a></li>
        <li><a href="https://openpyxl.readthedocs.io/">openpyxl</a></li>
        <li><a href="http://github.com/ActiveState/appdirs">appdirs</a></li>
        <li><a href="https://matplotlib.org/">matplotlib</a></li>
        <li><a href="https://github.com/Miksus/red-mail">redmail</a></li>
    </ul>
</p>

<h2 id="support">
    {_("Support")}
</h2>
<h3>
    {_("Buy me a `coffee`:")}
</h3>  

![{_("Buy me a \"coffee\".")}]\
({_("https://raw.githubusercontent.com/larryw3i/funingschool/master"+
"/Documentation/images/9237879a-f8d5-11ee-8411-23057db0a773.jpeg")})

<h2 id="license">
    {_("License")}
</h2>

<a href="{_("https://github.com/larryw3i/funingschool/blob/master/LICENSE")}">
    GNU LESSER GENERAL PUBLIC LICENSE Version 3
</a>
"""
        )


# The end.
