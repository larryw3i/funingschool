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
        self._cls_cfg_fpath = None
        self._user_cfg_fpath = None

    @property
    def cfg(self):
        if not self._cfg:
            self._cfg = Config(self)
        return self._cfg
        pass

    @property
    def dpath(self):
        if not self._dpath:
            dpath = get_share_dpath(
                Path(inspect.getfile(self.__class__))
            )
            dpath = dpath.parent / dpath.stem
            self._dpath = dpath

        return self._dpath

    @property
    def cls_cfg_fpath(self):
        if not self._cls_cfg_fpath:
            self._cls_cfg_fpath = self.dpath / (_("config") + ".toml")
        return self._cls_cfg_fpath

    @property
    def user_cfg_fpath(self):
        if not self._user_cfg_fpath:
            self._user_cfg_fpath = self.user.cfg_fpath
        return self._user_cfg_fpath
        pass

    @property
    def user(self, cls_cfg=None):
        if not self._user:
            self._user = User(self)
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        pass


# The end.
