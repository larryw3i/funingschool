import matplotlib
import matplotlib.font_manager as fm
from fnschool.language import *

if is_zh_CN:
    ttves = fm.fontManager.ttflist
    ttves = [
        f.name
        for f in ttves
        if (
            "hei" in f.name.lower()
            or "cjk" in f.name.lower()
            or "kai" in f.name.lower()
            or "song" in f.name.lower()
            or "ming" in f.name.lower()
        )
    ]
    random.shuffle(ttves)
    matplotlib.rcParams["font.family"] = ttves
