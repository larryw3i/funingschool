
import os
import sys
from pathlib import Path
import shutil
import tomllib

from fnschool import *
from fnschool.canteen import *
from fnschool.canteen.path import *

class Friend:
    def __init__(
        self, label=None, name=None, email=None, school=None, suppliers=None
    ):
        self.label = label
        self.name = name
        self.email = email
        self.school = school
        self.suppliers = suppliers


    def get_friend_by_label(self, label):
        friends = self.get_friends()
        for f in friends:
            if f.label == label:
                return f

        return None


    def get_friends(self):
        friends = []
        _friends = None
        
        with open(friends_fpath,'r') as f:
            _friends = tomllib.load(f)
            _friends = friends["canteen"]["friends"]

        for _f in _friends:
            friends.append(
                Friend(
                    label=_f[0],
                    name=_f[1],
                    email=_f[2],
                    school=_f[3],
                    suppliers=_f[4],
                )
            )
        return friends


# The end.
