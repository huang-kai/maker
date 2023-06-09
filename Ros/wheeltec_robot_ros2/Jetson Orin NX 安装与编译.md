# Jetson Orin NX 安装与编译
wheeltec的文档比较乱，整理一下我的安装方法。此文档基于ROS2 galactic 版本，其他版本类同。
## 1. 安装ROS2 galactic
### 1.1 安装主程序
```
# 设置字符集
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings

# 加入ROS2 GPG key
sudo apt update && sudo apt install curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 加入 Repo
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# 安装
sudo apt update
sudo apt upgrade
sudo apt install ros-galactic-desktop

```
### 1.2 安装工具
```
# 安装补全工具
sudo apt install -y python3-pip
pip3 install -U argcomplete

# 安装编译工具
sudo apt install python3-colcon-common-extensions

# 安装依赖
sudo apt update && sudo apt install -y \
build-essential \
cmake \
git \
python3-flake8 \
python3-pytest-cov \
python3-rosdep \
python3-setuptools \
python3-vcstool \
wget

# 安装测试工具
python3 -m pip install -U \
flake8-blind-except \
flake8-builtins \
flake8-class-newline \
flake8-comprehensions \
flake8-deprecated \
flake8-docstrings \
flake8-import-order \
flake8-quotes \
pytest-repeat \
pytest-rerunfailures \
pytest \
setuptools

# 安装依赖项
python3 -m pip install -U importlib-metadata importlib-resources

# 设置环境变量
vim ~/.zshrc
# alias initros1="source /opt/ros/noetic/setup.zsh"
alias initros2="source /opt/ros/galactic/setup.zsh"
source ~/.zshrc
```

### 1.3 验证安装
```
initros2
# 再两个终端上分别运行
ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_py listener
```

## 2. 编译wheeltec的ROS2代码
### 2.1 创建workspace并上传代码
```
mkdir -p ~/dev/wheeltec_robot_ros2/src

# 上传代码此过程略
```

### 2.2 安装依赖
```
# 使用rosdep安装依赖
rosdep init
rosdep update

cd ~/dev/wheeltec_robot_ros2
rosdep install --from-paths src --ignore-src -r -y --rosdistro galactic
# 运行完成后会显示#all required rosdeps installed successfully

# 安装其他依赖
sudo apt install -y ros-galactic-usb-cam \
                    ros-galactic-async-web-server-cpp \
                    ros-galactic-test-msgs \
                    ros-galactic-behaviortree-cpp-v3 \
                    ros-galactic-ompl \
                    ros-galactic-filters \
                    ros-galactic-diagnostic-updater \
                    ros-galactic-gazebo-ros-pkgs \
                    ros-galactic-test-msgs \
                    ros-galactic-behaviortree-cpp-v3 \
                    


```

### 2.3 编译步骤
```
# 先编译 rrt msg
colcon build --packages-select wheeltec_rrt_msg
. install/setup.zsh
```

### 2.4 奥比深度相机代码编译
#### step1 安装相机依赖
```
sudo apt install libgflags-dev nlohmann-json3-dev \
                               ros-galactic-image-transport \
                               ros-galactic-image-publisher 
```
#### step2 安装其他依赖
```
# 安装glog
cd ~/dev/git/github.com
git clone https://github.com/google/glog
cd glog
git checkout v0.6.0
mkdir build && cd build
cmake .. && make -j4
sudo make install
sudo ldconfig

# 安装magic_enum 
cd ~/dev/git/github.com
git clone https://github.com/Neargye/magic_enu
cd magic_enu
git checkout v0.8.0
cd magic_enum-0.8.0
mkdir build && cd build
cmake .. && make -j4
sudo make install
sudo ldconfig 

# 安装libuvc 
git clone https://github.com/libuvc/libuvc.git
cd libuvc
mkdir build && cd build
cmake .. && make -j4
sudo make install
sudo ldconfig 
```
#### step3 映射串口
```
cd ~/dev/wheeltec_robot_ros2/src/ros2_astra_camera/astra_camera/scripts
sudo bash install.sh
sudo udevadm control --reload-rules && sudo udevadm trigger
```

#### step4 编译
```
cd ~/wheeltec_ws
source /opt/ros/galactic/setup.bash
colcon build --packages-select astra_camera_msgs
colcon build --packages-select astra_camera
```

#### 报错处理
出现如下报错
```
Target "astra_camera" links to target "LibUVC::UVCShared" but the target
was not found. Perhaps a find_package() call is missing for an IMPORTED
target, or an ALIAS target is missing?
```
解决办法，修改 `ros2_astra_camera/astra_camera` 文件夹下的 `CMakeLists.txt`，
将 `LibUVC::UVCShared` 修改为`${libuvc_LIBRARIES}`，保存后编译即可。

## 3. 运行
### 3.1 安装依赖
```
sudo apt install -y ros-galactic-joint-state-publisher \
                    ros-galactic-robot-localization \
                    ros-galactic-robot-state-publisher \
```

### 3.2 映射串口号
```
vim ~/dev/wheeltec_robot_ros2/src/turn_on_wheeltec_robot/wheeltec_udev_new.sh

#CP2102 串口号0002 设置别名为wheeltec_controller
echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60",ATTRS{serial}=="0002", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_controller"' >/etc/udev/rules.d/wheeltec_controller.rules
#CH9102，同时系统安装了对应驱动 串口号0002 设置别名为wheeltec_controller
echo  'KERNEL=="ttyCH343USB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4",ATTRS{serial}=="0002", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_controller"' >/etc/udev/rules.d/wheeltec_controller2.rules
#CH9102，同时系统没有安装对应驱动 串口号0002 设置别名为wheeltec_controller
echo  'KERNEL=="ttyACM*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4",ATTRS{serial}=="0002", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_controller"' >/etc/udev/rules.d/wheeltec_controller3.rules

#CP2102 串口号0001 设置别名为wheeltec_lidar
echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60",ATTRS{serial}=="0001", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_lidar"' >/etc/udev/rules.d/wheeltec_lidar.rules
#CH9102，同时系统安装了对应驱动 串口号0001 设置别名为wheeltec_lidar
echo  'KERNEL=="ttyCH343USB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4",ATTRS{serial}=="54B8001974", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_lidar"' >/etc/udev/rules.d/wheeltec_lidar2.rules
#CH9102，同时系统没有安装对应驱动 串口号0001 设置别名为wheeltec_lidar
echo  'KERNEL=="ttyACM*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4",ATTRS{serial}=="0001", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_lidar"' >/etc/udev/rules.d/wheeltec_lidar3.rules

#CP2102 串口号0003 设置别名为wheeltec_FDI_IMU_GNSS
echo  'KERNEL=="ttyUSB*", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60",ATTRS{serial}=="0003", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_FDI_IMU_GNSS"' >/etc/udev/rules.d/wheeltec_fdi_imu_gnss.rules
#CH9102，同时系统安装了对应驱动 串口号0003 设置别名为wheeltec_FDI_IMU_GNSS
echo  'KERNEL=="ttyCH343USB*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4",ATTRS{serial}=="0003", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_FDI_IMU_GNSS"' >/etc/udev/rules.d/wheeltec_fdi_imu_gnss2.rules
#CH9102，同时系统没有安装对应驱动 串口号0003 设置别名为wheeltec_FDI_IMU_GNSS
echo  'KERNEL=="ttyACM*", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="55d4",ATTRS{serial}=="0003", MODE:="0777", GROUP:="dialout", SYMLINK+="wheeltec_FDI_IMU_GNSS"' >/etc/udev/rules.d/wheeltec_fdi_imu_gnss3.rules

echo  'SUBSYSTEM=="video4linux",ATTR{name}=="GENERAL WEBCAM",ATTR{index}=="0",MODE:="0777",SYMLINK+="RgbCam"' >>/etc/udev/rules.d/camera.rules
echo  'SUBSYSTEM=="video4linux",ATTR{name}=="GENERAL WEBCAM: GENERAL WEBCAM",ATTR{index}=="0",MODE:="0777",SYMLINK+="RgbCam"' >>/etc/udev/rules.d/camera.rules
echo  'SUBSYSTEM=="video4linux",ATTR{name}=="Astra Pro HD Camera: Astra Pro ",ATTR{index}=="0",MODE:="0777",SYMLINK+="Astra_Pro"' >>/etc/udev/rules.d/camera.rules
echo  'SUBSYSTEM=="video4linux",ATTR{name}=="USB 2.0 Camera: USB Camera",ATTR{index}=="0",MODE:="0777",SYMLINK+="Astra_Dabai"' >>/etc/udev/rules.d/camera.rules
echo  'SUBSYSTEM=="video4linux",ATTR{name}=="USB 2.0 Camera",ATTR{index}=="0",MODE:="0777",SYMLINK+="Astra_Gemini"' >>/etc/udev/rules.d/camera.rules
echo  'SUBSYSTEM=="video4linux",ATTR{name}=="Intel(R) RealSense(TM) Depth Ca",ATTR{index}=="0",MODE:="0777",SYMLINK+="realsense"' >>/etc/udev/rules.d/camera.rules

service udev reload
sleep 2
service udev restart

sudo sh ~/dev/wheeltec_robot_ros2/src/turn_on_wheeltec_robot/wheeltec_udev.sh

# 插拔一下usb
ll /dev
# 看到 wheeltec_controller 说明映射成功
```
### 3.3 配置文件

### 3.3 启动
```
cd ~/dev/wheeltec_robot_ros2/
. install/setup.zsh

ros2 launch turn_on_wheeltec_robot turn_on_wheeltec_robot.launch.py

```