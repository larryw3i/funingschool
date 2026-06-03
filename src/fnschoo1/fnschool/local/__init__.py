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


def get_local(*args, **kwargs):
    request = kwargs.get("request")
    lang = request.COOKIES.get("django_language")
    lang_module_name = lang.replace("-", "_").replace(".", "_").lower()
    lang_module_names = [
        p.stem for p in (Path(__file__).parent).glob("*.py") if p.is_file()
    ]
    lang_module_name = (
        lang_module_name if lang_module_name in lang_module_names else "en"
    )
    lang_module = import_module(f"fnschool.local.{lang_module_name}")
    local = lang_module.get_local(*args, **kwargs)
    return local


# The end.
