import os
import sys
from pathlib import Path
import shutil
import calendar
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

from tkinter import filedialog

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *
from fnschool.canteen.spreadsheet.purchasing import Purchasing
from fnschool.canteen.spreadsheet.consuming import Consuming
from fnschool.canteen.spreadsheet.preconsuming import PreConsuming
from fnschool.canteen.spreadsheet.inventory import Inventory
from fnschool.canteen.spreadsheet.warehousing import Warehousing
from fnschool.canteen.spreadsheet.cover import Cover


class CtSpreadSheet:
    def __init__(self, bill):
        self.bill = bill
        self._preconsuming = None
        self._purchasing = None
        self._consuming = None
        self._inventory = None
        self._warehousing = None
        self._cover = None

    @property
    def cover(self):
        if not self._cover:
            self._cover = Cover(self.bill)
        return self._cover

    @property
    def warehousing(self):
       if not self._warehousing:
           sel._warehousing = Warehousing(self.bill)
        return self._warehousing

    @property
    def purchasing(self):
        if not self._purchasing:
            self._purchasing = Purchasing(self.bill)
        return self._purchasing

    @property
    def preconsuming(self):
        if not self._preconsuming:
            self._preconsuming = PreConsuming(self.bill)
        return self._preconsuming

    @property
    def consuming(self):
        if not self._consuming:
            self._consuming = Consuming(self.bill)
        return self._consuming

    @property
    def inventory(self):
        if not self._inventory:
            self._inventory = Inventory(self.bill)
        return self._inventory
    
    def update(self):
        self.
        pass

# The end.
