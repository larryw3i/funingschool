import os
import sys

from fnschool import *


class ConfigBase:
    def __init__(self, cfg_fpath):
        self._path = cfg_fpath
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

    def save(self):
        data = self.data
        with open(self.path, "w", encoding="utf-8") as f:
            tomlkit.dump(data, f)
            pass
        print_info(_("Configuration data has been saved!"))
        pass


class ClsConfig(ConfigBase):
    def __init__(self, cfg_fpath=None):
        cfg_fpath = cfg_fpath or (
            Path(self.__class__).parent / (_("config") + ".toml")
        )
        cfg_fpath = get_config_dpath(cfg_fpath)
        super().__init__(cfg_fpath)
        pass


class UserConfig(ConfigBase):
    def __init__(self, user):
        self.user = user
        cfg_fpath = self.user.cfg_fpath
        super().__init__(cfg_fpath)


class AppConfig(ConfigBase):
    def __init__(self, cfg_fpath=None):
        cfg_fpath = cfg_fpath or app_config_fpath
        super().__init__(self, cfg_fpath)

        pass

    pass


# The end.
