import os
import sys
import random

app_name = "fnschool"
app_author = "larryw3i"
app_version = None


def get_app_version():

    global app_version
    if not app_version:
        from fnschool import __version__

        app_version = __version__
    return app_version


def print_app():

    app_name = random.choice(
        [
            [
                r" _____ _   _ ____   ____ _   _  ___   ___  _     ",
                r"|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    ",
                r"| |_  |  \| \___ \| |   | |_| | | | | | | | |    ",
                r"|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ ",
                r"|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|",
                r"",
            ],
            [
                r"|`````````````````````````````````````````````````|",
                r"| _____ _   _ ____   ____ _   _  ___   ___  _     |",
                r"||  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    |",
                r"|| |_  |  \| \___ \| |   | |_| | | | | | | | |    |",
                r"||  _| | |\  |___) | |___|  _  | |_| | |_| | |___ |",
                r"||_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____||",
                r"|                                                 |",
                r"```````````````````````````````````````````````````",
                r"",
            ],
            [
                "",
                "  ▄▄                ▗▖             ▗▄▖ ",
                " ▐▛▀                ▐▌             ▝▜▌ ",
                "▐███ ▐▙██▖▗▟██▖ ▟██▖▐▙██▖ ▟█▙  ▟█▙  ▐▌ ",
                " ▐▌  ▐▛ ▐▌▐▙▄▖▘▐▛  ▘▐▛ ▐▌▐▛ ▜▌▐▛ ▜▌ ▐▌ ",
                " ▐▌  ▐▌ ▐▌ ▀▀█▖▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌ ▐▌ ",
                " ▐▌  ▐▌ ▐▌▐▄▄▟▌▝█▄▄▌▐▌ ▐▌▝█▄█▘▝█▄█▘ ▐▙▄",
                " ▝▘  ▝▘ ▝▘ ▀▀▀  ▝▀▀ ▝▘ ▝▘ ▝▀▘  ▝▀▘   ▀▀",
                "",
            ],
            [
                " _______________________________________",
                "|  ▄▄                ▗▖             ▗▄▖ |",
                "| ▐▛▀                ▐▌             ▝▜▌ |",
                "|▐███ ▐▙██▖▗▟██▖ ▟██▖▐▙██▖ ▟█▙  ▟█▙  ▐▌ |",
                "| ▐▌  ▐▛ ▐▌▐▙▄▖▘▐▛  ▘▐▛ ▐▌▐▛ ▜▌▐▛ ▜▌ ▐▌ |",
                "| ▐▌  ▐▌ ▐▌ ▀▀█▖▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌ ▐▌ |",
                "| ▐▌  ▐▌ ▐▌▐▄▄▟▌▝█▄▄▌▐▌ ▐▌▝█▄█▘▝█▄█▘ ▐▙▄|",
                "| ▝▘  ▝▘ ▝▘ ▀▀▀  ▝▀▀ ▝▘ ▝▘ ▝▀▘  ▝▀▘   ▀▀|",
                "|_______________________________________|",
                "",
            ],
            [
                "",
                "▗▄▄▄▖▗▄ ▗▖ ▗▄▖   ▄▄ ▗▖ ▗▖ ▗▄▖  ▗▄▖ ▗▖   ",
                "▐▛▀▀▘▐█ ▐▌▗▛▀▜  █▀▀▌▐▌ ▐▌ █▀█  █▀█ ▐▌   ",
                "▐▌   ▐▛▌▐▌▐▙   ▐▛   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ",
                "▐███ ▐▌█▐▌ ▜█▙ ▐▌   ▐███▌▐▌ ▐▌▐▌ ▐▌▐▌   ",
                "▐▌   ▐▌▐▟▌   ▜▌▐▙   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ",
                "▐▌   ▐▌ █▌▐▄▄▟▘ █▄▄▌▐▌ ▐▌ █▄█  █▄█ ▐▙▄▄▖",
                "▝▘   ▝▘ ▀▘ ▀▀▘   ▀▀ ▝▘ ▝▘ ▝▀▘  ▝▀▘ ▝▀▀▀▘",
                "",
            ],
            [
                "============================================",
                "||▗▄▄▄▖▗▄ ▗▖ ▗▄▖   ▄▄ ▗▖ ▗▖ ▗▄▖  ▗▄▖ ▗▖   ||",
                "||▐▛▀▀▘▐█ ▐▌▗▛▀▜  █▀▀▌▐▌ ▐▌ █▀█  █▀█ ▐▌   ||",
                "||▐▌   ▐▛▌▐▌▐▙   ▐▛   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ||",
                "||▐███ ▐▌█▐▌ ▜█▙ ▐▌   ▐███▌▐▌ ▐▌▐▌ ▐▌▐▌   ||",
                "||▐▌   ▐▌▐▟▌   ▜▌▐▙   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌▐▌   ||",
                "||▐▌   ▐▌ █▌▐▄▄▟▘ █▄▄▌▐▌ ▐▌ █▄█  █▄█ ▐▙▄▄▖||",
                "||▝▘   ▝▘ ▀▘ ▀▀▘   ▀▀ ▝▘ ▝▘ ▝▀▘  ▝▀▘ ▝▀▀▀▘||",
                "============================================",
                "",
            ],
        ]
    )

    app_name_len = max([len(l) for l in app_name])
    version = "v" + get_app_version()
    version0 = f"{version:>{app_name_len}}"
    version1 = f"{version:^{app_name_len}}"

    app_name = "\n".join(app_name)
    version = random.choice([version0, version1])
    app_info = "\n" + app_name + version + "\n"
    print(app_info)


class App:
    def __init__(self):
        from fnschool.path import app_config_fpath

        self.cfg_fpath = app_config_fpath
        self._name = None
        self._version = None
        self._cfg = None
        self._ui = None
        self._use_tk = False
        pass

    @property
    def use_tk(self):
        return self._use_tk
        pass

    @use_tk.setter
    def use_tk(self, value=True):
        self._use_tk = value
        pass

    @property
    def name(self):
        if not self._name:
            self._name = app_name
        return self._name
        pass

    @property
    def version(self):
        if not self._version:
            self._version = get_app_version()
        return self._version
        pass

    @property
    def ui(self):
        if not self._ui:
            from fnschool.ui import UI

            self._ui = UI()
            pass
        return self._ui
        pass

    @property
    def cfg(self):
        from fnschool.config import AppConfig

        if not self._cfg:
            self._cfg = AppConfig(self)
        return self._cfg
        pass

    pass


# The end.
