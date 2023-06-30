#/bin/env python
#-*-coding:utf-8-*-
import filecmp
import os
import socket
import time
import smtplib
import urllib.request
from email.mime.text import MIMEText 

# 文件地址
file_path = '/home/jetson/dev/scripts/.last_ip_addr'

# 检查网络是否连接
def check_network():
    while True:
        try:
            result=urllib.request.urlopen('http://baidu.com').read()
            print(result)
            print("Network is Ready!")
            break
        except Exception:
            print("Network is not ready,Sleep 5s....")
            time.sleep(5)
    return True
 
# 获得本机指定接口的ip地址
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("1.1.1.1",80))
    ipaddr=s.getsockname()[0]
    s.close()
    print(ipaddr)
    return ipaddr
 
#将IP地址发到指定邮箱
def SendMe(ipaddr):
    smtp_server = 'smtp.qq.com'
    from_add = '17792336@qq.com'
    from_pwd = 'lbommndxsyvzbifc'
    to_add = ['17792336@qq.com']

    msg = MIMEText(ipaddr,'plain','utf-8')
    msg['From'] = from_add
    msg['To'] = to_add[0]
    msg['Subject'] = 'The IP address today'

    try:
        server = smtplib.SMTP_SSL(smtp_server,465)
        server.login(from_add,from_pwd)
        server.sendmail(from_add,to_add,msg.as_string())
        server.quit()
    except smtplin.SMTPException as e:
        print('error',e)
 
#简单比较一下是否发生改变，以决定是否发送邮件
if __name__ == '__main__':
    check_network()
    ipaddr=get_ip_address()
    if not os.path.exists(file_path):
        print("IP address changed. Send E-mail to me!")
        SendMe(ipaddr)
        with open(file_path, 'w') as file:
            file.write(ipaddr)
        exit(0)

    # 读取文件内容
    with open(file_path, 'r') as file:
        last_ip_addr = file.read()

    if last_ip_addr != ipaddr:
        print("IP address changed. Send E-mail to me!")
        SendMe(ipaddr)
        with open(file_path, 'w') as file:
            file.write(ipaddr)
    else:
        print("IP address not changed. Do nothing!")