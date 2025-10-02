from helper import *
from helper.project.info import Info as ProjectInfo


class Msg:
    def __init__(self):
        self._proj = None
        self._project_dpaths = None
        pass

    @property
    def proj(self):
        if not self._proj:
            proj = ProjectInfo()
            self._proj = proj
        return self._proj

    def get_pot_fpath(self, dpath):
        fpath = self.get_locales_dpath(dpath) / (dpath.stem + ".pot")
        return fpath

    def get_locales_dpath(self, dpath):
        dpath = dpath / "locales"
        if not dpath.exists():
            os.makedirs(dpath, exist_ok=True)
        return dpath

    @property
    def project_dpaths(self):
        if not self._project_dpaths:
            dpaths = self.proj.dpaths + [helper_dpath]
            self._project_dpaths = dpaths
        return self._project_dpaths

    def update(self):
        for dpath in self.project_dpaths:
            module_name = dpath.stem
            dpath_r = dpath.relative_to(project_dpath)
            pot_path = self.get_pot_fpath(dpath)
            locales_dpath = self.get_locales_dpath(dpath)
            sh_value = (
                f"pybabel extract {dpath_r}"
                + f" -o {pot_path};"
                + f"pybabel update"
                + f" -i {pot_path}"
                + f" -d {locales_dpath}"
                + f" -D {module_name}"
            )
            sh(sh_value)

    def compile(self):
        for dpath in self.project_dpaths:
            module_name = dpath.stem
            dpath_r = dpath.relative_to(project_dpath)
            pot_path = self.get_pot_fpath(dpath)
            locales_dpath = self.get_locales_dpath(dpath)

            sh_value = (
                f"pybabel compile"
                + f" -d {locales_dpath}"
                + f" -D {module_name}"
            )

            sh(sh_value)

    def add(self, language_code):
        language_code = language_code
        for dpath in self.project_dpaths:
            module_name = dpath.stem
            dpath_r = dpath.relative_to(project_dpath)
            pot_path = self.get_pot_fpath(dpath)
            locales_dpath = self.get_locales_dpath(dpath)

            sh_value = (
                f"pybabel init"
                + f" -d {locales_dpath}"
                + f" -l {language_code}"
                + f" -i {pot_path}"
                + f" -D {module_name}"
            )
            sh(sh_value)


# The end.
