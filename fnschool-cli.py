#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

import sys
PROJECT_PATH=Path(__file__).parent
FNSCHOOL_PATH=PROJECT_PATH/"src"/"fnschool"
if FNSCHOOL_PATH.as_posix() not in sys.path:
    sys.path.append(FNSCHOOL_PATH.as_posix())

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fnschool.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
