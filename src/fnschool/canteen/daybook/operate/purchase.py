import os
import sys

from fnschool import *
from fnschool.canteen.daybook.operate import *
from fnschool.canteen.daybook.operate.base import *


class NonIgnorableGoods(OprBase):
    def __init__(self, note):
        OprBase.__init__(note)
        pass


class NonIgnorableGoodsSum(OprBase):
    def __init__(self, note):
        OprBase.__init__(self, note)
        pass


class IgnorableGoods(OprBase):
    def __init__(self, note):
        OprBase.__init__(self, note)
        pass


class IgnorableGoodsSum(OprBase):
    def __init__(self, note):
        OprBase.__init__(self, note)
        pass


class Purchase(OprBase):
    def __init__(self, note):
        OprBase.__init__(self, note)
        self._pfoods = None

        pass

    @property
    def pfoods(self):
        if not self._pfoods:
            from tkinter import scrolledtext

            window = tk.Tk()
            width = int(self.ui.screen_width / 2)
            height = int(self.ui.screen_height / 2)
            window.title(_("Select spreadsheet"))
            window.geometry(f"{width}x{height}")
            window.resizable(False, False)
            window.columnconfigure(0, weight=1)
            window.rowconfigure(0, weight=1)
            tip_txt = scrolledtext.ScrolledText(
                window,
            )
            tip_txt.grid(column=0, row=0, sticky="EWSN")
            s_btn = tk.Button(
                text=_("OK! Select a purchased foods spreadsheet,")
            )
            tip_txt.insert(tk.INSERT, self.select_pfoods_file_str)
            tip_txt.configure(state="disabled")
            s_btn.grid(column=0, row=1, sticky="E")
            s_btn.focus_set()
            window.mainloop()
            pass

        return self._pfoods


# The end.
