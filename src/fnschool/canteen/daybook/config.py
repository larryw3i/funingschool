import os
import sys

from fnschool import *
from fnschool.canteen.path import *


class CtConfig(Config):
    def __init__(self, config_fpath):
        super().__init__(config_fpath)
