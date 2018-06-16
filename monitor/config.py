#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 下午4:28
# @Author  : cxy
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @desc    :
import time,datetime

TODAY = time.time()
TIME_PATH = str(TODAY.year) + "/" + str(TODAY.month) + "/" + str(datetime.datetime.now().date())

MONITOR_CONFIG = {
    "monitor_file":[
        {"key":"py_distribute-datacollect","path":"/home/vagrant/py_distribute/data/" + TIME_PATH + "_error.txt","max_size":100},
    ],
    "send_account":"xxxx@qq.com",
    "license_code":"feruwfpsiwkuibge", # 授权码
    "rec_account":["xxxx@qq.com"],
    "host":"smtp.qq.com",
    "port":465,
    "sleep_time":60,
}