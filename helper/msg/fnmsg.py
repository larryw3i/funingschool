from helper import *

from helper.project.fnproject import Project


class Msg:
    def __init__(self):
        self._proj = None
        self._project_dpaths = None
        pass

    @property
    def proj(self):
        if not self._proj:
            proj = Project()
            self._proj = proj
        return self._proj

    def get_pot_fpath(self, dpath):
        fpath = self.get_locales_dpath(dpath) / (dpath.stem + ".pot")
        return fpath

    def get_locales_dpath(self, dpath):
        dpath = dpath / "locales"
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
                f"pybabel extract {dpath_r} -o {pot_path};"
                + f"pybabel update -i {pot_path} -d {locales_dpath} -D {module_name}"
            )
            sh(sh_value)

    def compile(self):
        for dpath in self.project_dpaths:
            module_name = dpath.stem
            dpath_r = dpath.relative_to(project_dpath)
            pot_path = self.get_pot_fpath(dpath)
            locales_dpath = self.get_locales_dpath(dpath)

            sh_value = f"pybabel compile -d {locales_dpath} -D {module_name}"
            sh(sh_value)

    def add(self, language_code):
        for dpath in self.project_dpaths:
            module_name = dpath.stem
            dpath_r = dpath.relative_to(project_dpath)
            pot_path = self.get_pot_fpath(dpath)
            locales_dpath = self.get_locales_dpath(dpath)

            sh_value = (
                f"pybabel init -d {locales_dpath} -l {language_code} "
                + f"-i {pot_path} -D {module_name}"
            )
            sh(sh_value)


# The end.
