
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
    不只是一些出入库设计。
</h4>
<hr/>
<p align="center">
    <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/README/zh_CN.md">简体中文</a> •
    <a href="https://github.com/larryw3i/funingschool/blob/master/README.md">English</a>
</p>

<p align="center">
    <a href="#key-features">
        特性
    </a>
    •
    <a href="#how-to-use">
        如何使用
    </a>
    •
    <a href="#credits">
        致谢（声明）
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

![截图](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/44e58998-da32-11f0-b726-700894a38a35.png)

<h2 id="key-features">
    特性
</h2>

<h3>
    食材出入库
</h3>

* 自动读取食材表单。
* 更简单更直观食材出库设计。
* 自动更新表单（入库、出库、汇总等等）。
* 减少计算误差。
* 有效地“消除”含有无限小数的单价。
* 在工作薄之间合并食材台账。  
* 易用。

<h2 id="how-to-use">
    如何使用
</h2>

<h3>
    安装 Python3
</h3>
<p>

在 `Debian` 上：

```bash
sudo apt-get install python3 python3-pip python3-tk
```  
在 `Windows 10` 或 `Windows 11` 上，您可以从以下链接获得二进制安装程序（请自行检验哈希值）：  
* https://registry.npmmirror.com/binary.html?path=python/  
* https://mirrors.huaweicloud.com/python/  
* https://mirror.bjtu.edu.cn/python/  

（`fnschool` 需要 Python 3.12 或 3.12 以上 的运行环境。）
</p>

<h3>
    安装 和 运行 fnschool 
</h3>

<p>

运行 命令行 应用：
* `Debian`：`Ctrl+Alt+T`；  
* `Windows`：“`Win+R，powershell，回车`”。  

然后执行如下命令：

</p>

```bash
# 设置安装源为镜像站。
pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple # 或
pip config set global.index-url https://mirror.nju.edu.cn/pypi/web/simple # 或
pip config set global.index-url https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple  

# 安装 fnschool 。
pip install -U fnschool
# 更新数据库。
python -m fnschoo1.manage migrate
# 启动 fnschoo1。
python -m fnschoo1.manage 
```
<h2 id="credits">
    致谢（声明）
</h2>
<p>
    此软件使用了如下的开源软件包（项目）：
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
    GNU LESSER GENERAL PUBLIC LICENSE Version 3
</a>
