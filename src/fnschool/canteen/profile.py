import os
import sys
from pathlib import Path
import shutil
import tomllib

from fnschool import *
from fnschool.path import *
from fnschool.canteen import *
from fnschool.canteen.path import *
from fnschool.canteen.config import *


class Profile:
    def __init__(
        self, label=None, name=None, email=None, org_name=None, suppliers=None
    ):
        self._label = label
        self.name = name
        self.email = email
        self.org_name = org_name
        self.suppliers = suppliers

    @property
    def label(self):
        return self._label.replace(" ", "")

    def get_profile_by_label(self, label):
        profiles = self.get_profiles()
        for f in profiles:
            if f.label == label:
                return f

        return None

    def get_profile0(self):
        profiles = self.get_profiles()
        if len(profiles) > 0:
            profile = profiles[0]
            return profile

        return None

    def get_profiles(self):
        profiles = []
        _profiles = Config().get_profiles()

        for _f in _profiles:
            profiles.append(
                Profile(
                    label=_f[0],
                    name=_f[1],
                    email=_f[2],
                    org_name=_f[3],
                    suppliers=_f[4],
                )
            )
        return profiles


# The end.
