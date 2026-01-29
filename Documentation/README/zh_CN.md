<hr/>
<div align="center">
   <pre>
 _____ _   _ ____   ____ _   _  ___   ___  _     
|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    
| |_  |  \| \___ \| |   | |_| | | | | | | | |    
|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ 
|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|
    </pre>
</div>
<p align="center">
    funingschool 
</p>

<h4 align="center">
    不只是一些出入库脚本。
</h4>
<hr/>
<p align="center">
    <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/README/zh_CN.md">简体中文</a> •
    <a href="https://github.com/larryw3i/funingschool/blob/master/Documentation/README/en_US.md">English</a>
</p>

<p align="center">
    <a href="#key-features">
         特性
    </a>
    •
    <a href="#how-to-use">
         使用
    </a>
    •
    <a href="#credits">
         鸣谢
    </a>
    •
    <a href="#support">
         赞助
    </a>
    •
    <a href="#license">
         授权
    </a>
</p>

<p align="center">
    <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/CHANGELOG/zh_CN.md">更新日志    </a>
</p>

![截屏](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/44e58998-da32-11f0-b726-700894a38a35.png)
<h2 id="key-features">
    特性
</h2>
<h3>
    出入库
</h3>

* 自动读取入库表格。
* 简单直接的消耗设计。
* 自动更新“入库、出库、汇总、盘存”等表格。
* 减少计算错误。
* 避免出现无限小数单价。
* 简单易用。
<h2 id="how-to-use">
    如何使用
</h2>
<h3>
安装 Python3
</h3>

<p>

在 `Debian` 或 `Ubuntu` 上：
```bash
sudo apt-get install python3 python3-pip python-is-python3
```  
对于 `Windows 10` 和 `Windows 11` ，你可以从以下网址获取 `Python3` 并安装：  
* https://www.python.org/getit/
* https://registry.npmmirror.com/binary.html?path=python/  
* https://mirrors.huaweicloud.com/python/  
* https://mirror.bjtu.edu.cn/python/  

（`funingschool` 需要 Python 3.12 或 3.12 以上版本）
</p>

<h3>
    安装 fnschool 并运行它
</h3>

<p>

运行`命令行`（航站楼）应用：
* `Debian 或 Ubuntu`：`Ctrl+Alt+T`。
* `Windows`："`Win+R（同时按）, 输入“powershell”, 按 Enter`"。

复制粘贴以下命令：

</p>

```bash
# 在 `Debian` 或 `Ubuntu` 机器上，你可能要使用虚拟环境，其命令：
python -m venv --system-site-packages ~/pyvenv; # 初次创建。
. ~/pyvenv/bin/activate; # 后续使用。
# 由于网络堵塞，安装 `fnschool` 时会出现访问不到 PyPI 源或网速慢的情形。由此，建议您设置访问源为镜像源，这样做便于您安装和更新：
pip config set global.extra-index-url "https://mirrors.pku.edu.cn/pypi/web/simple https://mirror.nju.edu.cn/pypi/web/simple https://mirrors.ustc.edu.cn/pypi/web/simple https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple https://mirrors.zju.edu.cn/pypi/web/simple https://mirror.sjtu.edu.cn/pypi/web/simple"
# 安装 或 更新 `fnschool` 。
pip install -U fnschool
# 更新数据库。
python -m fnschoo1.manage migrate
# 启动 `fnschool` 。
python -m fnschoo1.manage
```
<h2 id="credits">
鸣谢
</h2>
<p>

此项目使用了以下的开源项目（包）：
   <ul>
       <li><a href="https://pandas.pydata.org/">pandas</a></li>
       <li><a href="https://numpy.org/">numpy</a></li>
       <li><a href="https://openpyxl.readthedocs.io/">openpyxl</a></li>
       <li><a href="https://github.com/tox-dev/platformdirs">platformdirs</a></li>
       <li><a href="https://matplotlib.org/">matplotlib</a></li>
   </ul>
</p>

<h2 id="support">
赞助
</h2>
<h3>
给我买一杯“咖啡”：
</h3>

![给我买一杯“咖啡”。](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/5ec0296a-8a3b-11ef-8e0b-efbca71f7f1a.png)
<h2 id="license">
授权
</h2>
<a href="https://gitee.com/larryw3i/funingschool/blob/master/LICENSE">
GNU 宽通用公共许可证 第3版
</a>