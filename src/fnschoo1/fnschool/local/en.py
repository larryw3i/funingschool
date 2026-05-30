import calendar
import io
import math
import os
import random
import re
import zipfile
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from django.utils import translation
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from fnschool.local.base import FnLocal


class FnEnLocal(FnLocal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def get_char_count(text):
        return len(text)

    def get_numeral(self, num):
        return num


def get_local():
    en_local = FnEnLocal()
    return en_local


# The end.
