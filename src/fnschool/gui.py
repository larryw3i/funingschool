import os
import sys
import tkinter as tk
from pygubu.widgets.simpletooltip import Tooltip


class Gui:
    def __init__(self):
        self._screen_height = None
        self._screen_width = None
        pass

    @property
    def screen_width(self):
        if not self._screen_width:
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            self._screen_width = int(screen_width)
            root.destroy()
        return self._screen_width
        pass

    @property
    def screen_height(self):
        if not self._screen_height:
            root = tk.Tk()
            screen_height = root.winfo_screenheight()
            self._screen_height = int(screen_height)
            root.destroy()
        return self._screen_height
        pass

    def show_info(self, content, title=_("Information"), root=None):
        info_window = tk.Toplevel(root) if root else tk.Tk()
        if root:
            info_window.transient(root)

        info_window.title(title)
        w, h = int(self.screen_width / 4), int(self.screen_height / 4)
        info_window.geometry(f"{w}x{h}")

        main_frame = tk.Frame(info_window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        border_frame = tk.Frame(main_frame, bg="pink", bd=2, relief=tk.SOLID)
        border_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        content_text = tk.Text(
            border_frame,
            wrap=tk.WORD,
            bg="pink",
            fg="black",
            font=("Mono", 10),
            padx=10,
            pady=10,
            height=10,
        )
        content_text.insert("1.0", content)
        content_text["state"] = "disabled"
        content_text.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 10))

        ok_button = tk.Button(
            bottom_frame,
            text="OK",
            command=info_window.destroy,
            width=10,
            height=1,
        )
        ok_button.pack(pady=5)

        if not root:
            info_window.mainloop()

    pass


# The end.
