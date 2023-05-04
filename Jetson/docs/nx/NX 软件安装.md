# NX 软件安装
## 1. Conda
[conda官网](https://docs.conda.io/en/latest/miniconda.html#installing)   
下载python3.8  aarch64版本
```
bash ~/Downloads/Miniconda3-py38_23.1.0-1-Linux-aarch64.sh
```

## 2. Nvidia pytorch
注意，pytorch官网的版本无法开启cuda，需要按照[Nvidia官方](https://docs.nvidia.com/deeplearning/frameworks/install-pytorch-jetson-platform/index.html)安装，这里以1.14版本举例，新版本可以从 https://developer.download.nvidia.cn/compute/redist/jp/v51/pytorch/ 寻找
```
# 安装依赖包
sudo apt-get -y update; 
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



