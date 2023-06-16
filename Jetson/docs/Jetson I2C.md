# Jetson I2C
## 1. 安装smbus库与配置——I2C
```
sudo apt-get install -y python3-smbus
sudo usermod -aG i2c <用户名>	    #添加用户组
sudo reboot 
sudo apt-get install -y i2c-tools
```

## 2. 链接NFC卡
身边只有itead公司生产的PN532 NFC卡，由于版本型号较老，这张卡只提供了26针的SPI接口，故使用I2C代替。
### 2.1 设置跳线
PN532卡上有两个跳线开关，设置成I2C模式
```
SET0-->H
SET1-->L
```
### 2.2 按照1的命令安装i2c并设置usermod
### 2.3 安装必要的应用包
```
sudo apt-get update
sudo apt-get install libusb-dev libpcsclite-dev

cd ~/Download
wget https://github.com/nfc-tools/libnfc/releases/download/libnfc-1.8.0/libnfc-1.8.0.tar.bz2
tar -xf libnfc-1.8.0.tar.bz2
cd libnfc-1.8.0 
./configure --prefix=/usr --sysconfdir=/etc
make &&sudo make install

# ubuntu系统需要拷贝权限文件
sudo cp contrib/udev/93-pn53x.rules /lib/udev/rules.d/
```
### 2.4 配置nfc
每一代的Jetson针脚对应的编号不一样，Nano系列只有8个I2C的接口，但Orin系列有12个I2C。首先需要寻找Jetson上IO的编号：
```
sudo /opt/nvidia/jetson-io/jetson-io.py
# 选：Configure Jetson 40pin Header
 =================== Jetson Expansion Header Tool ===================
 |                                                                    |
 |                                                                    |
 |                      3.3V (  1) .. (  2) 5V                        |
 |                      i2c8 (  3) .. (  4) 5V                        |
 |                      i2c8 (  5) .. (  6) GND                       |
 |                    unused (  7) .. (  8) uarta                     |
 |                       GND (  9) .. ( 10) uarta                     |
 |                    unused ( 11) .. ( 12) unused                    |
 |                    unused ( 13) .. ( 14) GND                       |
 |                    unused ( 15) .. ( 16) unused                    |
 |                      3.3V ( 17) .. ( 18) unused                    |
 |                    unused ( 19) .. ( 20) GND                       |
 |                    unused ( 21) .. ( 22) unused                    |
 |                    unused ( 23) .. ( 24) unused                    |
 |                       GND ( 25) .. ( 26) unused                    |
 |                      i2c2 ( 27) .. ( 28) i2c2                      |
 |                    unused ( 29) .. ( 30) GND                       |
 |                    unused ( 31) .. ( 32) unused                    |
 |                    unused ( 33) .. ( 34) GND                       |
 |                    unused ( 35) .. ( 36) unused                    |
 |                    unused ( 37) .. ( 38) unused                    |
 |                       GND ( 39) .. ( 40) unused                    |
 |                                                                    |
 |                                                                    |
 |                        Jetson 40pin Header:                        |
 |                                                                    |
 |                 Configure for compatible hardware                  |
 |                   Configure header pins manually                   |
 |                                Back                                |
 |                                                                    |
 |                                                                    |
  ====================================================================
```
可以看到3，5针脚对应的编号是i2c8。同时可以列出所有i2c
```
$ i2cdetect -l

i2c-3	i2c       	3190000.i2c                     	I2C adapter
i2c-10	i2c       	i2c-2-mux (chan_id 1)           	I2C adapter
i2c-1	i2c       	c240000.i2c                     	I2C adapter
i2c-8	i2c       	31e0000.i2c                     	I2C adapter
i2c-6	i2c       	31c0000.i2c                     	I2C adapter
i2c-4	i2c       	Tegra BPMP I2C adapter          	I2C adapter
i2c-11	i2c       	NVIDIA SOC i2c adapter 0        	I2C adapter
i2c-2	i2c       	3180000.i2c                     	I2C adapter
i2c-0	i2c       	3160000.i2c                     	I2C adapter
i2c-9	i2c       	i2c-2-mux (chan_id 0)           	I2C adapter
i2c-7	i2c       	c250000.i2c                     	I2C adapter
i2c-5	i2c       	31b0000.i2c                     	I2C adapter
```
我们可以扫描一下8号设备
```
$ sudo i2cdetect -y -r -a 8
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- 24 -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: UU -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

```
如果全是“--”则说明没有连接上设备。  

生成配置文件：
```
sudo mkdir -P /usr/local/etc/nfc
sudo vim /usr/local/etc/nfc/libnfc.conf

# Allow device auto-detection (default: true)
# Note: if this auto-detection is disabled, user has to manually set a device
# configuration using file or environment variable
allow_autoscan = true

# Allow intrusive auto-detection (default: false)
# Warning: intrusive auto-detection can seriously disturb other devices
# This option is not recommended, so user should prefer to add manually his/her device.
allow_intrusive_scan = false

# Set log level (default: error)
# Valid log levels are (in order of verbosity): 0 (none), 1 (error), 2 (info), 3 (debug)
# Note: if you compiled with --enable-debug option, the default log level is "debug"
log_level = 1

# Manually set default device (no default)
# To set a default device, users must set both name and connstring for their device
# Note: if autoscan is enabled, default device will be the first device available in device list.
device.name = "Itead_PN532"
device.connstring = "pn532_i2c:/dev/i2c-7"
```

### 2.5 硬件连接
如图所示  
![](resources/rpi_pn532_9.webp)

### 2.6 读写NFC
至此，配置已经完成
使用命令进行测试：
```
LIBNFC_LOG_LEVEL=3 nfc-list -v
nfc-list
# 如果nfc上有卡，则会读取卡中信息
nfc-list uses libnfc 1.8.0
NFC device: Itead_PN532 opened
1 ISO14443A passive target(s) found:
ISO/IEC 14443A (106 kbps) target:
    ATQA (SENS_RES): 00  04
       UID (NFCID1): 86  45  c4  9f
      SAK (SEL_RES): 28
                ATS: 78  80  b0  02  20  90  00  00  00  00  00  86  45  c4  9f
```
如果门禁卡的 SAK 是 08，是可以被mfoc破解复制的，如果为 20 的话，需要使用mfuck
```
# 官网下载mfoc
git clone https://github.com/nfc-tools/mfoc
cd mfoc 
autoreconf -is
./configure
make && sudo make install
```
破解卡片信息
```
sudo mfoc -O bak.mfd
```
如果最后运行没有报错，那么 mfoc 就已经成功备份出门禁的数据 bak.mfd 了  

如果mfoc不能直接破解，则需要使用mfuck+mfoc进行破解
mfcuk (MiFare Classic Universal toolKit) 是一款基于 dackside 攻击原理破解全加密 M1 卡的开源软件，mfcuk 通过算法的漏洞破解出第一个 key，如果某个扇区的 key 被破解出来，就可以再使用 mfoc 工具使用 nested authentication 攻击破解其他扇区的密码。
```
# 安装mfuck
git clone https://github.com/nfc-tools/mfcuk
cd mfuck
autoreconf -is
./configure
make

# 进行破解
sudo ./mfcuk -C -R 0:A -s 250 -S 250 -v 3
# 破解过程很久，直到出现
INFO: block 4 recovered KEY: 3c5d7f1e.
```
得到第一个 key 之后，我就可以跟退出 mfcuk ，通过获取到的 key，使用 mfoc 进行再次解密
```
sudo mfoc -k 3c5d7f1e -O bak.mfd
```
如果 mfcuk 破解的第一个 key 是正确的，mfoc 命令一般会在几分钟之内完成整个 M1 卡所有扇区的破解，最终将成功生成导出备份文件。

写入新卡,使用 libnfc 软件包自带的 `nfc-mfclassic` 命令进行写卡，可以通过`nfc-mfclassic -h`获得帮助
```
nfc-mfclassic w a u bak.mfd
```

### 最后
可以看到使用的工具都是利用了m1卡的漏洞进行破解，所以一张门禁卡能不能复制就要看这个门禁卡有没有漏洞，如果是最近一两年才新加装的门禁系统，估计已经没有这些漏洞可以利用了。
