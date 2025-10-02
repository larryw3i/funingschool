import os
import sys
import tkinter as tk
import tomllib
from tkinter import filedialog, ttk

from openpyxl.utils.cell import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

from fnschool import *
from fnschool.canteen.food import *
from fnschool.canteen.path import *
from fnschool.canteen.spreadsheet.base import *


class FoodClass:
    def __init__(self, name, likes):
        self.name = name
        self.likes = likes
        pass


class FoodClasses:
    def __init__(self):
        pass

    @property
    def value(self):
        value0 = []
        value1 = value0 if is_zh_CN else value0
        return value1


# The end.
