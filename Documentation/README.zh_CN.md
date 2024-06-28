
<h1 align="center">
  <br>
  
  <pre>
 _____ _   _ ____   ____ _   _  ___   ___  _     
|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    
| |_  |  \| \___ \| |   | |_| | | | | | | | |    
|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ 
|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|
                                                 
</pre>

  <br>
  funingschool
  <br>
</h1>

<h4 align="center"> 不仅仅是一些简单的做账脚本。 </h4>

<p align="center">
  <a href="https://gitee.com/larryw3i/funingschool/blob/master/Documentation/README.zh_CN.md">简体中文</a> •
  <a href="https://gitee.com/larryw3i/funingschool/blob/master/README.md">English</a>
</p>

<p align="center">
  <a href="#特点">特点</a> •
  <a href="#如何使用">如何使用</a> •
  <a href="#致谢">致谢</a> •
  <a href="#赞助">赞助</a> •
  <a href="#许可">许可</a>
</p>

![screenshot](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/de61adde-f8cc-11ee-ae9d-ff2db36858da.png)

## 特点
### 出入库设计
* 自动读取食材文件。  
* 直观且简单的消耗设计。  
* 自动更新表格（入库、出库、盘存等等）。  
* 减少计算错误。  
* 有效地消除含有无限小数的单价。
* 易用。  
### 测试统计
* 简明扼要的"测试成绩录入表格"。
* 一目了然的测试结果，把表格数据转换为直观的图片。
* 显示评语。
* 有效地帮助测试人员和被测试人员，尤其是老师们和学生们。

## 如何使用

### 安装 Python3  

#### Ubuntu：  
```bash
sudo apt-get install python3 python3-pip
```
#### Windows：  
下载 Python3 ，然后安装它。  
##### 可供使用的下载站点（请自行和对哈希值）：
* https://registry.npmmirror.com/binary.html?path=python/  
* https://mirrors.huaweicloud.com/python/  
* https://mirror.bjtu.edu.cn/python/

### 安装和运行 fnschool   
```bash
# 更换 PYPI 源为镜像站点
pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple
# 安装
pip3 install -U fnschool
# 运行出入库模块
fnschool-cli canteen mk_bill
# 运行成绩统计模块
fnschool-cli exam enter
```

> **注意**  
> 耐心认真阅读它提示的信息，这是你能运用好它的关键。  


## 致谢

这个项目使用到以下开源软件：

- [colorama](https://github.com/tartley/colorama)  
- [pandas](https://pandas.pydata.org/)  
- [numpy](https://numpy.org/)  
- [openpyxl](https://openpyxl.readthedocs.io/)  
- [appdirs](http://github.com/ActiveState/appdirs)  
- [matplotlib](https://matplotlib.org/)  


## 赞助

给我买杯“咖啡”：   

![Buy me a coffee](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/9237879a-f8d5-11ee-8411-23057db0a773.jpeg)

## 许可  

[GNU LESSER GENERAL PUBLIC LICENSE Version 3](https://gitee.com/larryw3i/funingschool/blob/master/LICENSE)



