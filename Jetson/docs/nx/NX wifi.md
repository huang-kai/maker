# NX wifi
## AX210 
驱动下载地址：https://www.intel.com/content/www/us/en/support/articles/000005511/wireless.html   
问题修复：
* https://askubuntu.com/questions/1360175/intel-wifi-6-ax210-wifi-not-working-after-update
* https://forums.developer.nvidia.com/t/intel-ax210-failed-to-evaluate-dsm-messages/236289
* https://bugzilla.kernel.org/show_bug.cgi?id=212371


## 更新 4.22
目前无法完美支持AX210，原因是wifi驱动可以适配，但是蓝牙驱动需要内核5.11+。蓝牙是USB设备（可以通过`lsusb`查看），但AX210会出现错误，导致usb无法正常使用，时间一长Orin nx会死机。期待官方升级内核到5.11+


## 更新 12.14
终于迎来了jetpack 6 DP 的升级，L4T也成功升级到了ubuntu 22.04版本，内核```5.15.122-tegra```。  
欣喜的是蓝牙部分已经完全兼容，但wifi还是不能用！根据
https://forums.developer.nvidia.com/t/faild-to-connect-wi-fi-network-on-jetson-linux-36-2/275212/2  
和  
https://zhuanlan.zhihu.com/p/586474020?utm_id=0  
中的方法，猜测在制作jetpack 6的时候没有对backports进行升级导致。着手对backports进行升级   

克隆backport仓库

```
git clone https://github.com/intel/backport-iwlwifi.git
cd backport-iwlwifi
```
进入iwlwifi-stack-dev文件并编译
```
cd iwlwifi-stack-dev
sudo make defconfig-iwlwifi-public
sudo make
sudo make install
```
下载驱动文件
```
git clone https://kernel.googlesource.com/pub/scm/linux/kernel/git/firmware/linux-firmware
cd linux-firmware/
sudo cp iwlwifi-* /lib/firmware
```
重启后查看dmesg
```
sudo dmesg |grep wifi
[   10.565817] Loading modules backported from iwlwifi
[   10.565822] iwlwifi-stack-dev:tags/jenkins-Core_build_core74_pv-44^0:jenkins-Core_build_core74_pv-60:128e12f4202f
[   10.631041] iwlwifi 0001:01:00.0: Adding to iommu group 3
[   10.634914] iwlwifi 0001:01:00.0: enabling device (0000 -> 0002)
[   10.636615] iwlwifi 0001:01:00.0: Detected crf-id 0x400410, cnv-id 0x400410 wfpm id 0x80000000
[   10.636623] iwlwifi 0001:01:00.0: PCI dev 2725/0024, rev=0x420, rfid=0x10d000
```
从界面上也能找到wifi，至此，AX210已经能再Orin Nx上使用了！




