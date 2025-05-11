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


# The end.
