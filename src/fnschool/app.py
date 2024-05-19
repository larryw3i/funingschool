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
    app_name0 = [
        r" _____ _   _ ____   ____ _   _  ___   ___  _     ",
        r"|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    ",
        r"| |_  |  \| \___ \| |   | |_| | | | | | | | |    ",
        r"|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ ",
        r"|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|",
        r"",
    ]
    app_name1 = [
        r"|`````````````````````````````````````````````````|",
        r"| _____ _   _ ____   ____ _   _  ___   ___  _     |",
        r"||  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    |",
        r"|| |_  |  \| \___ \| |   | |_| | | | | | | | |    |",
        r"||  _| | |\  |___) | |___|  _  | |_| | |_| | |___ |",
        r"||_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____||",
        r"|                                                 |",
        r"```````````````````````````````````````````````````",
        r"",
    ]
    app_name2 = [
        "",
        "  ▄▄                ▗▖             ▗▄▖ ",
        " ▐▛▀                ▐▌             ▝▜▌ ",
        "▐███ ▐▙██▖▗▟██▖ ▟██▖▐▙██▖ ▟█▙  ▟█▙  ▐▌ ",
        " ▐▌  ▐▛ ▐▌▐▙▄▖▘▐▛  ▘▐▛ ▐▌▐▛ ▜▌▐▛ ▜▌ ▐▌ ",
        " ▐▌  ▐▌ ▐▌ ▀▀█▖▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌ ▐▌ ",
        " ▐▌  ▐▌ ▐▌▐▄▄▟▌▝█▄▄▌▐▌ ▐▌▝█▄█▘▝█▄█▘ ▐▙▄",
        " ▝▘  ▝▘ ▝▘ ▀▀▀  ▝▀▀ ▝▘ ▝▘ ▝▀▘  ▝▀▘   ▀▀",
        "",
    ]
    app_name3 = [
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
    ]

    app_name = random.choice([app_name0, app_name1, app_name2, app_name3])

    app_name_len = max([len(l) for l in app_name])
    version = "v" + get_app_version()
    version0 = f"{version:>{app_name_len}}"
    version1 = f"{version:^{app_name_len}}"

    app_name = "\n".join(app_name)
    version = random.choice([version0, version1])
    app_info = "\n" + app_name + version + "\n"
    print(app_info)


# The end.
