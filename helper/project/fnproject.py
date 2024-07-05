import tomllib

from helper import *
from helper.project import *


class Project:
    def __init__(self):
        self._data = None
        self._deps = None
        self._dpaths = None
        pass

    def update(self):
        version_p = r'__version__ = ["|\'][0-9]{8}.8[0-9]{4}.8[0-9]{2}["|\']'
        ndate = datetime.now()
        version = ndate.strftime("%Y%m%d.8%H%M.8%S")
        for dpath in self.dpaths:
            init_fpath = dpath / "__init__.py"
            with open(init_fpath, "r+") as f:
                content = f.read()
                content = re.sub(
                    version_p, f'__version__ = "{version}"', content
                )
                f.seek(0)
                f.truncate()
                f.write(content)
        print(
            _("Version was updated.")
            if len(self.dpaths) == 1
            else _("Versions were updated.")
        )

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
        deps = ["black", "pybabel", "twine", "build"]
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


# The end.
