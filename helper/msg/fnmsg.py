from helper import *


class Msg:  
    def __init__(self):
        self.fnschool_dpath = fnschool_path
        self.fnschool_pot_fpath = 
        pass

    def update():
        sh_value = (
            f"pybabel extract {self.fnschool_path_r} -o {pot_path};"
            + f"pybabel update -i {pot_path} -d {locale_dir} -D {app_name}"
        )


    def compile():
        sh_value = (f"pybabel compile -d {locale_dir} -D {app_name}")


    def add(language_code):
        sh_value = (
            f"pybabel init -d {locale_dir} -l {language_code} "
            + f"-i {pot_path} -D {app_name}"
        )


# The end.
