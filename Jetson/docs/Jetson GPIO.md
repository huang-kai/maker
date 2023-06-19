# Jetson GPIO
### 1. 安装Jetson GPIO
```
git clone https://github.com/NVIDIA/jetson-gpio 
sudo cp -R jetson-gpio /opt/nvidia/ 
cd /opt/nvidia/jetson-gpio
sudo python3 setup.py install
```
### 2. 设置用户权限与修改规则
```
sudo groupadd -f -r gpio
sudo usermod -a -G gpio <your_user_name>
sudo cp /opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d/
sudo udevadm control –reload-rules && sudo udevadm trigger
```

