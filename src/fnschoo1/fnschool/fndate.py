import calendar
import os
import sys
from datetime import date, datetime, timedelta


def parse_date(value):
    year, month, day = (
        (value.split("/"))
        if "/" in value
        else (
            (value.split("-"))
            if "-" in value
            else (
                (value.split("."))
                if "." in value
                else (value[0:4], value[4:6], value[6:])
            )
        )
    )
    year, month, day = int(year), int(month), int(day)
    max_day = calendar.monthrange(year, month)[1]
    if day > max_day:
        day = max_day
    if month > 12:
        month = 12
    parsed_date = date(year, month, day)
    return parsed_date


# The end.
