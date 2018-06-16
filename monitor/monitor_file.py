#-*- encoding: utf8 -*-
# 腾讯邮箱授权码
# feruwfpsiwkuibge

import smtplib
import logging
import time
import os
from email.mime.text import MIMEText
import config

FORMAT = '[%(asctime)-15s] %(message)s'
logging.basicConfig(filename = "monitor.txt", level = logging.DEBUG, filemode = "a", format=FORMAT)

def get_file_size(file_name):
    if os.path.exists(file_name):
        bytes_size = float(os.path.getsize(file_name))
        kb = bytes_size/1024
        mb = kb/1024
        return mb
    return 0

def send_email(file_name,key):
    msg = MIMEText(file_name+"文件超过限制，可能存在异常，请处理。项目为："+key)
    msg = [key]
    msg["From"]= config["send_account"]
    msg["To"] = config["rec_account"]
    try:
        s = smtplib.SMTP_SSL(config["host"],config["port"])
        s.login(config["send_account"],config["license_code"])
        s.sendmail(config["send_account"],config["rec_account"],msg.as_string())
        s.quit()
        logging.info(file_name + "警告发送成功")
    except Exception as e:
        logging.exception(e)

# check
while True:
    for file in config["monitor_file"]:
        file_size = get_file_size(file["path"])
        if file_size > file["max_size"]:
            send_email(file["path"],file["key"])
    logging.info("检查完毕")
    time.sleep(config.MONITOR_CONFIG["sleep_time"])