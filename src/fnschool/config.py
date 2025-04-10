import os
import sys

from fnschool import *


class Config:
    def __init__(self, cfg_path):
        self._path = cfg_path
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

        pass


class ConfigBase(Config):

    def __init__(self, cfg_path):
        super().__init__(self, cfg_path)
        self._app_config = None
        pass

    @property
    def app_config(self):
        if not self._app_config:
            if not app_config_fpath.exists():
                with open(app_config_fpath, "w", encoding="utf-8") as f:
                    f.write("")
                    pass

                return {}

            app_config = Config(app_config_fpath)
            self._app_config = app_config
            pass

        return self._app_config
        pass

    pass


# The end.
