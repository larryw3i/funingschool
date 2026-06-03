import calendar
import io
import math
import os
import random
import re
import zipfile
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from importlib import import_module
from pathlib import Path

from django.utils import translation
from django.utils.translation import gettext as _

lang = translation.get_language()
lang_module_name = lang.replace("-", "_").replace(".", "_").lower()
lang_module_names = [
    p.stem for p in (Path(__file__).parent).glob("*.py") if p.is_file()
]
lang_module_name = (
    lang_module_name if lang_module_name in lang_module_names else "en"
)

is_zh_CN = lang.lower() in ["zh-cn", "zh-hans"]
is_zh_Hans = lang.lower() in ["zh-cn", "zh-hans"]
print(is_zh_Hans, is_zh_CN)


def get_local():
    lang_module = import_module(f"fnschool.local.{lang_module_name}")
    local = lang_module.get_local()
    return local


# The end.
