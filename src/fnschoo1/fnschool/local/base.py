import os
import sys
from pathlib import Path

from django.conf import settings


class FnLocal:
    def __init__(self, *args, **kwargs):
        self.request = kwargs.get("request", None)
        self.lang_code = self.request.COOKIES.get(
            "django_language", settings.LANGUAGE_CODE
        )
        self.is_zh_CN = self.lang_code.lower() in ["zh-cn", "zh-hans"]
        self.is_zh_Hans = self.lang_code.lower() in ["zh-cn", "zh-hans"]
        pass

    def get_monetary_amount(self, num):
        return num
        pass

    def get_char_count(self, value):
        return len(value)
        pass


# The end.
