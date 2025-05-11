import os
import sys
from abc import ABC
from pathlib import Path

from fnschool.base import *
from fnschool.user import *
from fnschool.path import *
from fnschool.config import *


class ClsBase(ABC):
    def __init__(self):
        self._dpath = None
        self._user = None
        self._cfg_fpath = None
        self._cfg = None
        self._app_cfg = None
        pass

    @property
    def cfg(self):
        if not self._cfg:
            self._cfg = ClsConfig(self.cfg_fpath)
        return self._cfg
        pass

    @property
    def dpath(self):
        if not self._dpath:
            dpath = get_share_dpath(Path(inspect.getfile(self.__class__)))
            dpath = dpath.parent / dpath.stem
            self._dpath = dpath

        return self._dpath

    @property
    def cfg_fpath(self):
        if not self._cfg_fpath:
            self._cfg_fpath = self.dpath / (_("config") + ".toml")
        return self._cfg_fpath

    @property
    def user(self):
        if not self._user:
            self._user = User(self)
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        pass

    @property
    def app_cfg(self):
        if not self._app_cfg:
            self._app_cfg = AppConfig(app_config_fpath)
        return self._app_cfg
        pass


# The end.
