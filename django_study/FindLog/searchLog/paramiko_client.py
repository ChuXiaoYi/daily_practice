#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 下午6:43
# @Author  : cxy
# @Site    : 
# @File    : paramiko_client.py
# @Software: PyCharm
# @desc    :
import paramiko
import configparser


class ParamikoClient(object):
    def __init__(self, config_str, section):
        self.config = configparser.ConfigParser()
        self.config.read(config_str)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sftp_client = None
        self.client_status = 0
        self.section = section

    def connect(self):
        try:
            self.client.connect(hostname=self.config.get(self.section, 'host'),
                                port=self.config.get(self.section, 'port'),
                                username=self.config.get(self.section, 'username'),
                                password=self.config.get(self.section, 'password'),
                                timeout=self.config.getfloat(self.section, 'timeout'),
                                )
            self.client_status = 1
        except Exception as e:
            print(e)
            try:
                self.client.close()
            except:
                pass

    def exec_commond(self, commond):
        stdin, stdout, stderr = self.client.exec_command(command=commond)
        return stdout
