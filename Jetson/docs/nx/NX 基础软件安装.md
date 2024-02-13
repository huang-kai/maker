# NX 基础软件安装
## 1. [Oh My Zsh](https://ohmyz.sh/)
```
sudo apt install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# 配置 omz
vim ~/.zshrc

ZSH_THEME="ys"
plugins=(git
         zsh-autosuggestions
         zsh-syntax-highlighting
         z
        )
alias ll='ls -alF'

proxy () {
  export all_proxy="10.249.6.238:1080"
  export http_proxy="10.249.6.238:1080"
  export https_proxy="10.249.6.238:1080"
  echo "Proxy on"
}

# where noproxy
noproxy () {
  unset all_proxy
  unset http_proxy
  unset https_proxy
  echo "Proxy off"
}

# 安装插件
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

```
## 2. 设置环境变量
### 2.1 CUDA
```
vim ~/.zsh

...
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=$CUDA_HOME:/usr/local/cuda
```

## 3. pip3
NX 初始安装的是python3.8 和 python2.7，我们暂时不用2.7版本，所以只安装python3.8的工具
```
sudo apt install -y python-is-python3
sudo apt install -y python3-pip

# 更换清华源
# 注意安装好的pip是老版本，首先更新一下pip
sudo -H python3 -m pip install --upgrade pip  

# 永久更换源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

```

## 4. jstat
```
sudo pip3 install -U jetson-stats
jtop
```
### 4.1 通过Jtop增加Swap分区
NX默认只有3.6GB的Swap区，在编译一些程序如moveit2的时候会报错。通过`jtop`的`4MEO`可以增加swap大小。

## 5. Conda
[conda官网](https://docs.conda.io/en/latest/miniconda.html#installing)   
下载python3.8  aarch64版本
```
bash ~/Downloads/Miniconda3-py38_<version>-Linux-aarch64.sh
```

## 6. Nvidia pytorch
注意，pytorch官网的版本无法开启cuda，需要按照[Nvidia官方](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html)安装，这里以1.14版本举例，新版本可以从 https://developer.download.nvidia.cn/compute/redist/jp/v51/pytorch/ 寻找
```
# 安装依赖包
sudo apt-get update; 
sudo apt-get -y install autoconf bc build-essential g++-8 gcc-8 clang-8 lld-8 gettext-base gfortran-8 iputils-ping libbz2-dev libc++-dev libcgal-dev libffi-dev libfreetype6-dev libhdf5-dev libjpeg-dev liblzma-dev libncurses5-dev libncursesw5-dev libpng-dev libreadline-dev libssl-dev libsqlite3-dev libxml2-dev libxslt-dev locales moreutils openssl python-openssl rsync scons python3-pip libopenblas-dev;

# 创建conda环境
conda create -n pytorch python=3.8

#安装 pytorch
export TORCH_INSTALL=https://developer.download.nvidia.cn/compute/redist/jp/v51/pytorch/torch-1.14.0a0+44dac51c.nv23.02-cp38-cp38-linux_aarch64.whl

python3 -m pip install --upgrade pip; python3 -m pip install aiohttp numpy=='1.19.4' scipy=='1.5.3'; export "LD_LIBRARY_PATH=/usr/lib/llvm-8/lib:$LD_LIBRARY_PATH"; python3 -m pip install --upgrade protobuf; python3 -m pip install --no-cache $TORCH_INSTALL

# 验证
 python3 -c  "import torch; print(torch.__version__); print(torch.cuda.is_available())"
 
```
## 7. 安装firefox（Ubuntu 22.04 没有默认安装的情况）
Ubuntu 22.04 中Firefox使用的snap包，但snap包有各种缺点，本方法使用dev包安装方式。 
```
# Step 1 删除snap包中的Firefox如有
snap list
sudo snap remove --purge firefox

# Step 2 添加 Mozilla team PPA 存储库
sudo add-apt-repository ppa:mozillateam/ppa

# Step 3 在 Ubuntu 22.04 LTS 上从 DEB 包安装 Firefox
sudo apt install --target-release 'o=LP-PPA-mozillateam' firefox
## --target-release选项可让您控制从何处下载安装包。因此，可以让apt使用mozillateam存储库作为源的命令。

# Step 4 更改 PPA 优先级
# Ubuntu 的官方仓库有版本号 1:1snap1-0ubuntu2，总是高于 PPA 包的版本。
# 系统希望将已安装的 Firefox 版本替换为其默认存储库中具有更高优先级的版本。其结果是又将 Firefox 恢复为 Snap。
# 因此，为避免这种情况发生，我们需要更改mozillateam存储库中数据包的优先级。为此，请运行以下命令：
sudo vim /etc/apt/preferences.d/mozillateamppa

Package: firefox*
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 501

sudo apt update
```

## 9. 删除无用软件
```
sudo apt remove deja-dup -y # 卸载备份工具
# sudo apt remove remmina -y # 卸载远程工具
sudo apt remove -y libreoffice-common # 卸载系统自带office
# sudo apt remove -y transmission-common # 卸载自带下载器
sudo apt remove -y aisleriot # 卸载系统自带的接龙游戏
sudo apt remove -y gnome-mahjongg # 卸载系统自带对对碰游戏
sudo apt remove -y gnome-mines # 卸载系统自带扫雷游戏
sudo apt remove -y gnome-sudoku # 卸载系统自带数独游戏
sudo apt remove -y rhythmbox # 卸载系统自带音乐播放器
sudo apt remove -y thunderbird # 卸载系统自带的邮件工具

sudo apt -y autoremove # 清理卸载软件依赖包

```

## 参考
1. https://conda.io/projects/conda/en/stable/user-guide/install/index.html
2. https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html
3. https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md
4. https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md
5. https://github.com/rbonghi/jetson_stats
6. https://www.linuxmi.com/ubuntu22-04-lts-firefox-deb.html

