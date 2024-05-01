import os
import sys
from pathlib import Path
from fnschool.log import *
from fnschool.language import _

time_nodes_dpath = Path(__file__).parent

time_node_banlun_fpath = time_node_banlun_fpath / "canteen.banlun.toml"
time_node_boai_fpath = time_node_banlun_fpath / "canteen.boai.toml"
time_node_dongbo_fpath = time_node_banlun_fpath / "canteen.dongbo.toml"
time_node_guichao_fpath = time_node_banlun_fpath / "canteen.guichao.toml"
time_node_gula_fpath = time_node_banlun_fpath / "canteen.gula.toml"
time_node_huajia_fpath = time_node_banlun_fpath / "canteen.huajia.toml"
time_node_lida_fpath = time_node_banlun_fpath / "canteen.lida.toml"
time_node_muyang_fpath = time_node_banlun_fpath / "canteen.muyang.toml"
time_node_naneng_fpath = time_node_banlun_fpath / "canteen.naneng.toml"
time_node_oyong_fpath = time_node_banlun_fpath / "canteen.oyong.toml"
time_node_tianpeng_fpath = time_node_banlun_fpath / "canteen.tianpeng.toml"
time_node_xinhua_fpath = time_node_banlun_fpath / "canteen.xinhua.toml"
time_node_zhesang_fpath = time_node_banlun_fpath / "canteen.zhesang.toml"


def get_time_node_fpath(region_name=None):
    names_path_list = [
        ["tianpeng", "田蓬", time_node_tianpeng_fpath],
        ["boai", "剥隘", time_node_boai_fpath],
        ["dongbo", "洞波", time_node_dongbo_fpath],
        ["guichao", "归朝", time_node_guichao_fpath],
        ["gula", "谷拉", time_node_gula_fpath],
        ["huajia", "花甲", time_node_huajia_fpath],
        ["lida", "里达", time_node_lida_fpath],
        ["muyang", "木央", time_node_muyang_fpath],
        ["naneng", "那能", time_node_naneng_fpath],
        ["oyong", "阿用", time_node_oyong_fpath],
        ["banlun", "板仑", time_node_banlun_fpath],
        ["xinhua", "新华", time_node_xinhua_fpath],
        ["zhesang", "者桑", time_node_zhesang_fpath],
    ]
    for names_path in names_path_list:
        if region_name in names_path[:-1]:
            return names_path[-1]

    print_info(
        _("There is no time nodes file for region name '{0}'.").format(
            region_name
        )
    )

    return None
