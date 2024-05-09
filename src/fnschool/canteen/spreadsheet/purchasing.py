
import os
import sys

from fnschool import *

class Purchasing():
    def __init__(self,bill):
        self.bill = bill


    @property
    def path(self):
        if not self._path:
            filetypes = ((_("Spreadsheet Files"), "*.xlsx"),)

            filename = filedialog.askopenfilename(
                title=_("Select the purchasing file"),
                initialdir=(Path.home() / "Downloads").as_posix(),
                filetypes=filetypes,
            )
            if filename is None:
                print_warning(_("No file was selected."))
                return None

            self._path = filename
        return self._path


