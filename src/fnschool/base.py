import os
import sys
from abc import ABC
from pathlib import Path

from fnschool.base import *
from fnschool.user import *
from fnschool.path import *
from fnschool.config import *


class ClsBase:
    def __init__(self):
        self._dpath = None
        self._user = None
        self._cfg = None
        self._mojo_cfg_fpath = None

    @property
    def cfg(self):
        if not self._cfg:
            self._cfg = Config(self)
        return self._cfg
        pass

    @property
    def dpath(self):
        if not self._dpath:
            self._dpath = get_share_dpath(
                Path(inspect.getfile(self.__class__)).parent
            )
        return self._dpath

    @property
    def mojo_cfg_fpath(self):
        if not self._mojo_cfg_fpath:
            self._mojo_cfg_fpath = self.dpath / (_("config") + ".toml")
        return self._mojo_cfg_fpath

    @property
    def user(self, mojo_cfg=None):
        if not self._user:
            self._user = User(self)
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        pass


# The end.
