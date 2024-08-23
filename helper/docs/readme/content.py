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
                with open(readme0_fpath,"w+",encoding="utf-8") as f:
                    f.write(content)
            readme_fpath = readme_dpath / f"README.{lc}.html"
            with open(readme_fpath,"w+",encoding="utf-8") as f:
                f.write(content)
            print(_("README file \"{0}\" was updated.").format(readme_fpath))

    
    def get_content(self, t_func = None):
        _ = t_func
        return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{_("README")}</title>
</head>
<body>
<h1 align="center">
  <br>
  
  <pre>
 _____ _   _ ____   ____ _   _  ___   ___  _     
|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    
| |_  |  \| \___ \| |   | |_| | | | | | | | |    
|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ 
|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|
                                                 
</pre>
     <br>
        {_("funingschool")}
    <br>
</h1>

<h4 align="center">
    {_("NO Just some simple scripts for warehousing and consuming.")}
</h4>

<p align="center">
  <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation\
/README.zh_CN.md">简体中文</a> •
  <a href="https://github.com/larryw3i/funingschool/blob/master/README.md">\
English</a>
</p>

<p align="center">
    <a href="#key-features">
        {_("Key Features")}
    </a> •
    <a href="#how-to-use">
        {_("How To Use")}
    </a> •
    <a href="#credits">
        {_("Credits")}
    </a> •
    <a href="#support">
        {_("Support")}
    </a> •
    <a href="#license">
        {_("License")}
    </a>
</p>

<img 
src="https://raw.githubusercontent.com/larryw3i/funingschool/master/\
Documentation/images/9432e132-f8cd-11ee-8ee6-f37309efa64b.png"\
 alt="Screenshot"
/>

<h2 name="key-features">
    {_("Key Features")}
</h2>
<h3>
    {_("warehousing and consuming")}
</h3>
<ol>
    <li>
        {_("Read food spreadsheets automatically.")}
    </li>
    <li>
        {_("The simplest and most straightforward `consuming sheets`.")}
    </li>
    <li>
        {_(
            "Update sheets (warehousing, consuming, "
            +"summing, etc) automatically."
        )}
    </li>
    <li>
        {_("Reduce calculation errors.")}
    </li>
    <li>
        {_("Effectively eliminate unit prices containing infinite decimals.")}
    </li>
    <li>
        {_("Easy to use.")}
    </li>
</ol>
<h3>
    {_("Test statistics")}
</h3>
<ol>
    <li>
        {_('An easy-to-use "test score entry form".')}
    </li>
    <li>
        {_(
            "Clear test results at a glance, "
            + "converting table data into Intuitive images."
        )}
    <li>
    <li>
        {_("Display comments.")}
    </li>
    <li>
        {_("Effectively assist testers, especially teachers and students.")}
    <li>
</ol>

<h2 name="how-to-use">
    {_("How To Use")}
</h2>
<h3>
    {_("Install Python3")}
</h3>
<p>
    Ubuntu:
    <pre>
        sudo apt-get install python3 python3-pip
    </pre>
    {_(
        "For `Windows`, you can install Python3 from "
        + "https://www.python.org/getit/ ."
    )}
</p>
<h3>
    {_("Install fnschool and run it")}
</h3>
<pre>
    # {_("install")}
    pip3 install -U fnschool
    # {_("run `warehousing and consuming` module")}
    fnschool-cli canteen mk_bill
    # { _("run `test statistics` module")}
    fnschool-cli exam enter
</pre>

<blockquote>
    {_("Note:")}
    {_(
        "Read the information it prompts carefully, "
        + "which is the key to using it well."
    )}
</blockquote>

<h2 name="credits">
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
<h2 name="support">
    {_("Support")}
</h2>
    {_("Buy me a `coffee`:")}
<img 
    src="https://raw.githubusercontent.com/larryw3i/funingschool/master\
/Documentation/images/9237879a-f8d5-11ee-8411-23057db0a773.jpeg"\
    alt='{_("Buy me a \"coffee\".")}'/>

<h2 name="license">
    {_("License")}
</h2>

<a href="https://github.com/larryw3i/funingschool/blob/master/LICENSE">
    GNU LESSER GENERAL PUBLIC LICENSE Version 3
</a>
</body>
"""


# The end.
