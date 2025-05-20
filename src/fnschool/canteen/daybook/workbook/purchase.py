import os
import sys

from fnschool.canteen.daybook.workbook import *


class Purchase(SheetBase):
    def __init__(self, spreadsheet):
        SheetBase.__init__(self, spreadsheet)
        self._foods = None
        pass

    @property
    def foods(self):
        if not self._foods:
            foods = None
            window = tk.Tk()
            width, height = (
                int(self.app.ui.screen_width / 2),
                int(self.app.ui.screen_height / 2),
            )
            window.geometry(f"{width}x{height}")
            window.title(_("Paste the purchasing data"))
            cols = [
                self.counting_date__strs[0],
                self.meal_type__strs[0],
                self.name_strs[0],
                self.quantity_strs[0],
                self.total_price_strs[0],
                self.residual_strs[0],
                self.negligible_strs[0],
            ]
            for i, col_title in enumerate(cols):
                row = 1
                col = i + 1
                svar = tk.StringVar()
                svar.set(col_title)
                col_label = tk.Label(window, textvariable=svar)
                col_label.grid(
                    row=row,
                    column=col,
                )
                fwidth = int(width / (len(cols)))
                frame = tk.Frame(
                    window,
                )
                frame.grid(row=row + 1, column=col, sticky="NS")
                window.grid_rowconfigure(row + 1, weight=1)
                window.grid_columnconfigure(col, weight=1)

                col_text = ScrolledText(frame)
                col_text.grid(row=1, column=1, sticky="WENS")
                frame.grid_rowconfigure(1, weight=1)
                frame.grid_columnconfigure(1, weight=1)
            row = 1
            select_file_btn = tk.Button(window, text=_("Select a file"))
            edit_btn = tk.Button(window, text=_("Edit"))
            select_file_btn.grid(row=row + 2, column=1, sticky="W")
            edit_btn.grid(row=row + 2, column=len(cols), sticky="E")

            window.mainloop()

        return self._foods

    pass


# The end.
