import tomllib

from helper import *
from helper.project import *


class Project:
    def __init__(self):
        self._data = None
        self._deps = None
        self._dpaths = None
        pass

    @property
    def dpaths(self):
        if not self._dpaths:
            dpaths = module_paths
            self._dpaths = dpaths
        return self._dpaths

    @property
    def data(self):
        if not self._data:
            data = None
            with open(project_toml_fpath, "rb") as f:
                data = tomllib.load(f)
            self._data = data

        return self._data

    @property
    def dev_deps(self):
        deps = [
            "black",
            "pybabel",
        ]
        return deps

    @property
    def deps(self):
        if not self._deps:
            deps = self.data["project"]["dependencies"]
            deps += self.dev_deps
            self._deps = deps
        return self._deps

    @property
    def deps_s(self):
        s = '"' + ('" "'.join(self.deps)) + '"'
        return s
