import os
import re
import sys


def count_chinese_characters(text):
    pattern = re.compile(r"[\u4e00-\u9fa5]")
    chinese_chars = pattern.findall(text)
    return len(chinese_chars)
