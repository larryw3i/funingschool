
<h1 align="center">
  <br>
  
  <pre> _____ _   _ ____   ____ _   _  ___   ___  _     
|  ___| \ | / ___| / ___| | | |/ _ \ / _ \| |    
| |_  |  \| \___ \| |   | |_| | | | | | | | |    
|  _| | |\  |___) | |___|  _  | |_| | |_| | |___ 
|_|   |_| \_|____/ \____|_| |_|\___/ \___/|_____|
                                                 
</pre>

  <br>
  funingschool
  <br>
</h1>

<h4 align="center"> 一些简单的做账脚本。 </h4>

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

* 自动读取食材文件。  
* 直观且简单的消耗设计。  
* 自动更新表格（入库、出库、盘存等等）。  
* 减少计算错误。  
* 易用。  

## 如何使用

### 安装 Python3  

Ubuntu：  
```bash
sudo apt-get install python3 python3-pip
```
Windows：  
从 [www.python.org/getit](https://www.python.org/getit/) 下载 Python3 ，然后安装它。  

### 安装和运行 fnschool   
```bash
# 更换 PYPI 源为镜像站点
pip config set global.index-url https://mirrors.bfsu.edu.cn/pypi/web/simple
# 安装
pip3 install -U fnschool
# 运行
fnschool-cli canteen mk_bill
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


## 赞助

给我买杯“咖啡”：   

![Buy me a coffee](https://gitee.com/larryw3i/funingschool/raw/master/Documentation/images/9237879a-f8d5-11ee-8411-23057db0a773.jpeg)

## 许可  

[GNU LESSER GENERAL PUBLIC LICENSE Version 3](https://gitee.com/larryw3i/funingschool/blob/master/LICENSE)



