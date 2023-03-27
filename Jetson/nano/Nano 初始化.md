# Nano 初始化
## 1. 硬件准备
### 1.1 安装网卡
nano开发板使用M.2 key接口网卡，打开开发板，网卡接口在芯片主板下，松开当中的螺丝，插入Intel 8267，拧上固定螺丝。
### 1.2 安装风扇
nano开发板上有四针带PWM功能的风扇接口，插入PWM风扇，并把风扇固定在散热器上。（注意如果不做设置，风扇是不会自己转的，后面介绍如何根据温度自动启动风扇）
## 2. SD卡初始化
首先去官网下载一个nano镜像，找一个读卡器插入SD卡，如果是空白卡，win11系统能认识并弹出U盘信息，使用SD card formatter会把SD卡格式化成Exfat格式。如果是Mac系统，选择格式化即可。打开烧录镜像软件[balenaEtcher](https://www.balena.io/etcher>)按照界面步骤烧录下载好的镜像，等完成后SD卡就准备完成了。  

### 2.1 使用Ubuntu 20.04版本镜像，可以参考[这篇文章](https://qengineering.eu/install-ubuntu-20.04-on-jetson-nano.html),或者直接[下载镜像]()  

## 3. 初次启动
把烧录好镜像的SD卡插入芯片板的插槽，注意不是开发板上。Nano支持3种供电方式  

    1. 5V2A的USB供电，最大功率10w
    2. 5V3A的GPIO供电，最大功率12W
    3. 5V3A的DC供电，最大功率15W  

推荐使用带开关的5V3A的DC供电，这样可以得到最大的使用性能。  
插入电源后，就等待出现Nvidia的启动画面，设置一些初始参数后便进入了系统。官方镜像使用18.20的Ubuntu版本，可以通过命令查看:
```
cat /etc/os-release

uname -a
```
### 3.1 安装一些系统包并换源
更换apt源
```
# 备份源文件
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak

# 使用国内源替换
sudo vim /etc/apt/sources.list

# 删除所有内容，并添加清华源，注意x86和arm64的源是不一样的

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-backports main restricted universe multiverse

# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security main restricted universe multiverse
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-security main restricted universe multiverse

deb http://ports.ubuntu.com/ubuntu-ports/ bionic-security main restricted universe multiverse
# deb-src http://ports.ubuntu.com/ubuntu-ports/ bionic-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-proposed main restricted universe multiverse
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu-ports/ bionic-proposed main restricted universe multiverse


$ sudo apt update
```
  
安装pip2/pip3
```
sudo apt install -y python-pip python3-pip

# 更换清华源
# 注意安装好的pip是9.0版本，首先更新一下pip
sudo -H python3 -m pip install --upgrade pip  

# 永久更换源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

```
### 3.2 安装基础Jetson包
```
# 1. 安装Jetpack
sudo apt install nvidia-jetpack
```