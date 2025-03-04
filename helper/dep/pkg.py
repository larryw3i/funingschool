import tomllib
from helper import *
from helper.project.info import Info


class Pkg:
    def __init__(self):
        self.venv_dpath = venv_dpath
        self._proj = None
        pass

    @property
    def proj(self):
        if not self._proj:

            self._proj = Project()
        return self._proj

    def install(self):
        sh_value = f"pip install -U {self.proj.deps_s};"
        sh(sh_value)
        print(
            (
                _("Dependency ({0}) has been installed.")
                if len(self.proj.deps) == 1
                else _("Dependencies ({0}) have been installed.")
            ).format(" ".join(self.proj.deps))
        )
        pass


# The end.
