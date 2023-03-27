# Nano风扇设置
## 手动控制风扇
```
sudo sh -c 'echo 100 > /sys/devices/pwm-fan/target_pwm'
```

## 自动控制风扇
```
git clone https://github.com/Pyrestone/jetson-fan-ctl.git
cd jetson-fan-ctl/ 
sudo ./install.sh

# 修改设置
sudo vim /etc/automagic-fan/config.json
{
    "FAN_OFF_TEMP":30,
    "FAN_MAX_TEMP":55,
    "UPDATE_INTERVAL":2,
    "MAX_PERF":1
}

# 修改后重启服务
sudo service automagic-fan restart
```  
`FAN_OFF_TEMP` 风扇开启的温度阈值  
`FAN_MAX_TEMP` 风扇100%运转的温度阈值.  
该脚本在这两点之间进行线性改动风扇的转速  

`UPDATE_INTERVAL` 脚本监控时间间隔.  
`MAX_PERF 设置大于` 0 表示将 CPU 和 GPU 时钟速度设置为最大值来最大化系统性能。

## 如果有问题可以通过命令查看
```
sudo service automagic-fan status
```