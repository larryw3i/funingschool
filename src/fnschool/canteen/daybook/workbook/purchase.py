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

        food_cols = {}

        def update_col_label(text, label_var):
            text_value = text.get("1.0", "end-1c")
            label_value = label_var.get()
            text_value_len = len(text_value.split("\n"))

            label_value_split = label_value.rsplit(_("("), 1)
            label_with_len = False
            if len(label_value_split) > 1:
                label_with_len = label_value_split[1].replace(_(")"), "")
                label_with_len = label_with_len.isnumeric()

            if label_with_len:
                label_value = label_value_split[0]

            label_value += _("({0})").format(text_value_len)
            label_var.set(label_value)

            pass

        def window_exit(root, texts):
            for col_title in texts.keys():
                text = texts[col_title]
                food_cols[col_title] = text.get("1.0", "end-1c")
            root.destroy()
            pass

        if not self._foods:
            foods = None
            texts = {}
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
                col_label_var = tk.StringVar()
                col_label_var.set(col_title)
                col_label = tk.Label(window, textvariable=col_label_var)
                col_label.grid(
                    row=row,
                    column=col,
                )
                col_frame = tk.Frame(
                    window,
                )
                col_frame.grid(row=row + 1, column=col, sticky="NS")
                window.grid_rowconfigure(row + 1, weight=1)
                window.grid_columnconfigure(col, weight=1)

                col_text = ScrolledText(col_frame)
                col_text.bind(
                    "<KeyRelease>",
                    lambda event, kwargs=dict(
                        text=col_text, label_var=col_label_var
                    ): (update_col_label(kwargs["text"], kwargs["label_var"])),
                )

                col_text.grid(row=1, column=1, sticky="WENS")
                col_frame.grid_rowconfigure(1, weight=1)
                col_frame.grid_columnconfigure(1, weight=1)
                texts[col_title] = col_text
                pass

            row = 1
            select_file_btn = tk.Button(window, text=_("Select a file"))
            edit_btn = tk.Button(window, text=_("Edit"))
            select_file_btn.grid(row=row + 2, column=1, sticky="W")
            edit_btn.grid(row=row + 2, column=len(cols), sticky="E")
            window.protocol(
                "WM_DELETE_WINDOW",
                lambda window=window, texts=texts: (window_exit(window, texts)),
            )
            window.mainloop()

            for col_title in food_cols.keys():
                col_data = food_cols[col_title]
                print(col_title)
                print(col_data)

        return self._foods

    pass


# The end.
