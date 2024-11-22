
import subprocess

from helper import *
from helper.msg.fnmsg import Msg
from helper.project.fnproject import Project

class Build():
    def __init__(self):
        pass

    def get_dists_hash(self):
        sh_value = (
            f"cd {dist_dpath}; "
            + f"sha256sum *; "
            + f"cd {project_dpath};"
        )
        hash_value = subprocess.check_output(sh_value, shell=True, universal_newlines=True)
        return hash_value

    def build(self, upload=False):
        msg = Msg() 
        proj = Project()

        msg.compile()
        proj.update()

        sh_value = (
            f"rm -rf {dist_fpaths}; "
            + f"python -m build;"
        )
        sh(sh_value)

        if upload:
            sh_value = (
                f"python -m twine upload {dist_fpaths}"
            )
            sh(sh_value)

            sha256_txt = None
            with open(sha256es_fpath, "r") as f:
                sha256_txt = f.read()
            hash_value = self.get_dists_hash()

            print(
                _("The hash value of distribution is:")
                if len(os.listdir(dist_dpath)) == 1 else _(
                    "The hash values of distributions are:"
                )
            )
            print(hash_value)

            sha256_txt = hash_value + sha256_txt
            with open(sha256es_fpath, "w+") as f:
                f.write(sha256_txt)
            print(f"SHA256 hash of '{dist_fpaths}'  was saved.")

        pass

# The end.
