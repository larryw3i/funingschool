
import os
import sys
from fnschool.exam import *

class Teacher():
    def __init__(
        self,
    ):
        self._name = None
        self._dpath = None
        pass
    
    @property
    def dpath(self):
        if not self._dpath:
           self._dpath = user_exam_dpath / self.name
           if not self._dpath.exists():
               os.makedirs(self._dpath,exist_ok=True)
        retunr self._dpath

    @property
    def name(self):
        if not self._name:
            print_info(_("Hey~ tell me your name, please:"))
            for i in range(0,3):
                self._name = input('>_ ').replace(' ','')
                if len(self._name) > 0:
                    break
                if i >= 2 :
                    print_error(_("Unexpected value was got. Exit"))
                    exit()
                else:
                    print_error(_("Unexpected value was got."))
        return self._name

    



