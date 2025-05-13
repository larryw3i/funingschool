import os
import sys

from fnschool import *
from abc import *


class OprBase(ABC):
    def __init__(self, note):
        self.note = note
        self.app = self.note.app
        self.ui = self.app.ui
        pass


# The end.
