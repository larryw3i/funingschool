import os
import sys

from helper import *
from helper.path import *

module_paths = [
   src_dpath/d for d in os.listdir(src_dpath)
   if "__init__.py" in os.listdir(src_dpath/d)
]
print(module_paths)

# The end.
