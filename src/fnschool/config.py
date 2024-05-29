import os
import sys

from fnschool import *


class Config:
    def __init__(self, path):
        self._path = path
        self._data = None

    @property
    def path(self):
        if not self._path.exists():
            with open(self._path, "w", encoding="utf-8") as f:
                f.write("")

        return self._path

    @property
    def data(self):
        if not self._data:
            with open(self.path, "rb") as f:
                self._data = tomllib.load(f)
            print_info(
                _("Configurations has been " + 'read from "{0}".').format(
                    self.path
                )
            )
        return self._data

    def get(self, key):
        value = self.data
        if key in value.keys():
            return value[key]
        return None

    def save(self, key, value):
        data = self.data
        if key in data.keys() and data[key] == value:
            return
        data[key] = value
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(
                "\n".join(
                    [f'"{key}"="{value0}"' for key, value0 in data.items()]
                )
            )
