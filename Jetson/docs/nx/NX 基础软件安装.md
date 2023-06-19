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

## 2. pip3
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

## 3. jstat
```
sudo pip3 install -U jetson-stats
jtop
```

## 4. Conda
[conda官网](https://docs.conda.io/en/latest/miniconda.html#installing)   
下载python3.8  aarch64版本
```
bash ~/Downloads/Miniconda3-py38_<version>-Linux-aarch64.sh
```

## 5. Nvidia pytorch
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
## 参考
1. https://conda.io/projects/conda/en/stable/user-guide/install/index.html
2. https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html
3. https://github.com/zsh-users/zsh-autosuggestions/blob/master/INSTALL.md
4. https://github.com/zsh-users/zsh-syntax-highlighting/blob/master/INSTALL.md
5. https://github.com/rbonghi/jetson_stats


