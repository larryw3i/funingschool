import os
import sys
from abc import ABC
from pathlib import Path

from fnschool.path import *
from fnschool.config import AppConfig

class ModuleBase(ABC):
    def __init__(self):
        self.config_path = get_config_dpath(Path(__file__))
        self._app_cfg = None
        self._mojo_cfg = None
        self._user_cfg = None

    @property
    def app_cfg(self):
        if not self._config:
            self._config = Config(self.config_path)

        return self._config
        pass

# The end.
