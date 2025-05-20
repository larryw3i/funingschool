import os
import sys
from fnschool.canteen.daybook.workbook import *
from fnschool.canteen.daybook.workbook.purchase import *


class SpreadSheet(FileBase):
    def __init__(self, note):
        FileBase.__init__(self, note)
        self._wb = None
        self._purchase = None
        self._fpath = None
        self._dpath = None

        pass

    def edit_workbook(self):
        self.wb.save(self.fpath)
        self.app.open_path(self.fpath)
        root = tk.Tk()
        messagebox.showinfo(
            root,
            _("Continue"),
            _('Edit opened Spreadsheet, save it and click "OK" to continue.'),
        )
        root.mainloop()
        self._wb = None

        pass

    @property
    def fpath(self):
        if not self._fpath:
            saved_wb_name_key = _("Saved Workbook Names")
            title = _("Select a spreadsheet")
            label = _("File:")
            tooltip = _("Select a saved file or enter a file name.")
            fpath = self.user.cfg.select(
                saved_wb_name_key, title, label, tooltip
            )
            self._fpath = self.dpath / fpath
        return self._fpath

    @property
    def dpath(self):
        if not self._dpath:
            self._dpath = self.user.dpath / _("Workbooks")
            if not self._dpath.exists():
                os.mkdirs(self._dpath)
                pass

        return self._dpath

    @property
    def wb(self):
        if not self._wb:
            if not sellf.fpath.exists():
                self._wb = Workbook()
            else:
                self._wb = load_workbook(self.fpath)
            pass
        return self._wb
        pass

    @property
    def purchase(self):
        if not self._purchase:
            self._purchase = Purchase(self)
        return self._purchase
        pass


# The end.
