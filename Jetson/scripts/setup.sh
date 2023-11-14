# !/bin/bash
mkdir -P /home/jetson/dev/scripts
cp get_ip.py /home/jetson/dev/scripts/
sudo chmod +x /home/jetson/dev/scripts/get_ip.py
sudo cp getIp.service /etc/systemd/system/
sudo systemctl start getIp.service
sudo systemctl enable getIp.service
