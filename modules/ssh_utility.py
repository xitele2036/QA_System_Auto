# -*- coding: utf-8 -*-
__author__ = 'Jason Liu'

import paramiko
import time

# def Singleton(cls):
#     _instance = {}
#
#     def _singleton(*args, **kargs):
#         if cls not in _instance:
#             _instance[cls] = cls(*args, **kargs)
#         return _instance[cls]
#
#     return _singleton
#
# @Singleton
class SSHUtility:

    # 初始化
    def __init__(self,usernames,passwords,hostnames):
        self.usernames = usernames
        self.passwords = passwords
        self.hostnames = hostnames
        # self.key = paramiko.RSAKey.from_private_key_file(
        #     "c:/Users/kliu/.ssh/known_hosts")
        self.s = paramiko.SSHClient()
        self.s.load_system_host_keys()
        # 允许连接不在know_hosts文件中的主机
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # 建立SSH连接
    def connect(self):
        self.s.connect(self.hostnames,22,self.usernames,self.passwords,allow_agent=True,look_for_keys=True)
    # 发送命令并返回原始结果
    def send(self,comm):
        stdin, stdout, stderr = self.s.exec_command(comm.encode())
        line = stdout.read()
        # print(line)
        return line.decode()

    # 关闭SSH连接
    def close(self):
        self.s.close()


if __name__ == '__main__':
    P759SH = SSHUtility('root',None,'10.86.79.139')
    P759SH.connect()
    log = P759SH.send("logcat")
    # print(log)






