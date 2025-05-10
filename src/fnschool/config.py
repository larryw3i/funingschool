import os
import sys

from abc import ABC
from fnschool import *


class ConfigBase(ABC):
    def __init__(self):
        self._data = None

    @property
    def path(self):

        if not self._cfg_fpath.exists():
            os.makedirs(self._cfg_fpath.parent, exist_ok=True)
            with open(self._cfg_fpath, "w", encoding="utf-8") as f:
                f.write("")
                pass

        return self._cfg_fpath

    @property
    def data(self):
        if not self._data:
            with open(self.path, "rb") as f:
                self._data = tomlkit.load(f)
                if not self._data:
                    self._data = {}
            print_info(
                _("Configurations has been " + 'read from "{0}".').format(
                    self.path
                )
            )
        return self._data
        pass

    def save(self):
        data = self.data
        with open(self.path, "w", encoding="utf-8") as f:
            tomlkit.dump(data, f)
            pass
        print_info(_("Configuration data has been saved!"))
        pass


class ClsConfig(ConfigBase):
    def __init__(self, cfg_fpath):
        self._cfg_fpath = cfg_fpath
        ConfigBase.__init__(self)
        pass


class UserConfig(ConfigBase):
    def __init__(self, cfg_fpath):
        self._cfg_fpath = cfg_fpath
        ConfigBase.__init__(self)


class AppConfig(ConfigBase):
    def __init__(self, cfg_fpath=None):
        self._cfg_fpath = cfg_fpath or app_config_fpath
        ConfigBase.__init__(self)

        pass

    pass


class Config:
    def __init__(self, cls):
        self.__cls = cls
        self.__cls_cfg_fpath = self.__cls.cls_cfg_fpath
        self._app = None
        self._user = None
        self._cls = None
        self.saved_user_names = None

    @property
    def app(self):
        if not self._app:
            self._app = AppConfig()
        return self._app

    @property
    def cls(self):
        if not self._cls:
            self._cls = ClsConfig(self.__cls_cfg_fpath)
        return self._cls

    @property
    def user(self):
        if not self._user:
            user = self.__cls.user
            self._user = user.cfg
        return self._user

    def save(self):
        for c in [self.app, self.cls, self.user]:
            c.save()
            print_info(
                _('Configuration file "{0}" has been saved!').format(
                    c._cfg_fpath
                )
            )
        pass

    pass


# The end.
