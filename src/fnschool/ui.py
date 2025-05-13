import os
import sys
import tkinter as tk


class UI:
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

    pass


# The end.
