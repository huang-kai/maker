# NX wifi
## AX210 
驱动下载地址：https://www.intel.com/content/www/us/en/support/articles/000005511/wireless.html   
问题修复：
* https://askubuntu.com/questions/1360175/intel-wifi-6-ax210-wifi-not-working-after-update
* https://forums.developer.nvidia.com/t/intel-ax210-failed-to-evaluate-dsm-messages/236289
* https://bugzilla.kernel.org/show_bug.cgi?id=212371


## 更新 4.22
目前无法完美支持AX210，原因是wifi驱动可以适配，但是蓝牙驱动需要内核5.11+。蓝牙是USB设备（可以通过`lsusb`查看），但AX210会出现错误，导致usb无法正常使用，时间一长Orin nx会死机。期待官方升级内核到5.11+



