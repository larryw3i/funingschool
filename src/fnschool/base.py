import os
import sys
from abc import ABC
from pathlib import Path

from fnschool.path import *
from fnschool.config import *


class MojoBase(MojoConfig):
    def __init__(self):
        self._app_cfg = None
        self._mojo_cfg = None
        self._user_cfg = None
        self._cfg_fpath = None
        self._dpath = None

    @property
    def dpath(self):
        if not self._dpath:
            self._dpath = get_share_dpath(
                Path(inspect.getfile(self.__class__).parent)
            )
        return self._dpath

    @property
    def cfg_fpath(self):
        if not self._cfg_fpath:
            self._cfg_fpath = self.dpath / (_("config") + ".toml")
        return self._cfg_fpath


# The end.
