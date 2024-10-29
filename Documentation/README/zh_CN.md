
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

![截图](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/9432e132-f8cd-11ee-8ee6-f37309efa64b.png)

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

<h3>
    测试统计
</h3>

* 易用的“测试登记”表单。
* 直观展示测试结果，生成直观的图片方便发送给学生家长。
* 显示测试备注。
* 有效协助测试相关人员，尤其是老师和学生。

<h2 id="how-to-use">
    如何使用
</h2>

<h3>
    安装 Python3
</h3>
<p>

在 `Ubuntu` 上：

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
* `Ubuntu`：`Ctrl+Alt+T`；  
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

# “食堂”模块的账单生成命令。
fnschool-cli canteen mk_bill
# “食堂”模块的合并食材台账命令。
fnschool-cli canteen merge_foodsheets

# 运行“测试”模块。
fnschool-cli exam enter
```

>备注：细心耐心阅读它打印的提示，这是您能使用好它的关键。

<h2 id="credits">
    致谢（声明）
</h2>
<p>
    此软件使用了如下的开源软件包（项目）：
    <ul>
        <li><a href="https://github.com/tartley/colorama">colorama</a></li>
        <li><a href="https://pandas.pydata.org/">pandas</a></li>
        <li><a href="https://numpy.org/">numpy</a></li>
        <li><a href="https://openpyxl.readthedocs.io/">openpyxl</a></li>
        <li><a href="http://github.com/ActiveState/appdirs">appdirs</a></li>
        <li><a href="https://matplotlib.org/">matplotlib</a></li>
        <li><a href="https://github.com/Miksus/red-mail">redmail</a></li>
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
