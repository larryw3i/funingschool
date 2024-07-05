
import tomllib
from helper import *
from helper.pkg.fnpkg import Pkg

class Dep:
    def __init__(self):
        self.venv_dpath = venv_dpath
        self._pkg = None 
        pass

    @property
    def pkg(self):
        if not self._pkg:
            pkg = Pkg()
            self._pkg = pkg
        return self._pkg

    def install(self):
        sh_value = f"pip install -U {self.pkg.deps_s};"
        sh(sh_value)
        print(
            (
                _("Dependencies ({0}) has been installed.")
                if len(self.pkg.deps) == 1 else 
                _("Dependencies ({0}) have been installed.")
            ).format(" ".join(self.pkg.deps))
        )
        pass



# The end.
