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

    def get(self):
        if not self._data:
            with open(self.path, "rb") as f:
                self._data = tomlkit.load(f)
            print_info(
                _("Configurations has been " + 'read from "{0}".').format(
                    self.path
                )
            )
        return self._data

    def save(self, key, value):
        data = self.data
        data[key] = value
        with open(self.path, "w", encoding="utf-8") as f:
            tomlkit.dump(data, f)

# The end.            
