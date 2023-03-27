# Nano I2C
### 1. 安装smbus库与配置——I2C
```
sudo apt-get install -y python3-smbus
sudo usermod -aG i2c <用户名>	    #添加用户组
sudo reboot 
sudo apt-get install -y i2c-tools
```