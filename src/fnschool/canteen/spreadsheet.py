import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np


from fnschool import *
from tkinter import filedialog


class SpreadSheet:
    def __init__(self, bill):
        self.bill = bill
        self._path = None

    @property
    def path(self):
        if not self._path:
            filetypes = ((_("Spreadsheet Files"), "*.xlsx"),)

            filename = filedialog.askopenfilename(
                title=_("Select a file"),
                initialdir=(Path.home() / "Downloads").as_posix(),
                filetypes=filetypes,
            )
            if filename is None:
                print_warning(_("No file was selected."))
                return None

            self._path = filename
        return self._path

    def read_foods(self):
        foods = pd.read_excel(self.path)
        print(foods)
        pass

    def design_consuming(self):
        pass

    def update_sheets(self):
        pass


# The end.
