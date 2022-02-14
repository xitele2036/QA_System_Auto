# -*- encoding:utf-8 -*-
import logging
import logging.config
import sys
from logging.handlers import TimedRotatingFileHandler
import os,time

class Logger(object):
    def __init__(self,logger):
        #创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.INFO)
        os.path.realpath(__file__)
        #创建一个hanlder，用于写入日志文件
        log_file_path = os.path.realpath(os.path.dirname(os.path.dirname(__file__)) +"/Logs")
        # print(log_file_path)
        logname = os.path.join(log_file_path, '{0}.log'.format(time.strftime('%Y-%m-%d-%H-%M-%S')))
        #logging模块自带的三个handler之一。继承自StreamHandler。将日志信息输出到磁盘文件上。
        fh = logging.FileHandler(logname)
        fh.setLevel(logging.INFO)
        #再创建一个handler，用于输出控制台
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        #定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #给handler设置格式
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        #给logger添加handler  换句话说就是给该logger添加不同的handler
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

    def getlog(self):
        return self.logger

logger = Logger('test').getlog()

# if __name__ == '__main__':
#     logger = Logger("test").getlog()
#     logger.info("hello")
