import os
import sys
from abc import ABC
from pathlib import Path

from fnschool.path import *

class ModuleBase(ABC):
    def __init__(self):
        self.config_path = get_config_dpath(Path(__file__))

        pass

# The end.
