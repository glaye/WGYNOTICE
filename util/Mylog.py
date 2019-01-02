import logging
import os
import time
import sys
from logging.handlers import RotatingFileHandler
from util import Readconf

cf = Readconf.Readconf().readConfigFile()
class logger:
    def __init__(self,
                 log_name=time.strftime("%Y-%m-%d.log", time.localtime())):
        '''
            set_level： 设置日志的打印级别，默认为DEBUG
            name： 日志中将会打印的name，默认为运行程序的name
            log_name： 日志文件的名字，默认为当前时间（年-月-日.log）
            log_path： 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
            use_console： 是否在控制台打印，默认为True
        '''
        set_level = cf.get('Mylog','set_level')

        log_path = os.path.join(cf.get('Mylog','log_path'),"logs")
        if sys.platform == 'win32': log_path = os.path.dirname(os.path.realpath(__file__))
        use_console = cf.get('Mylog','use_console')
#        print(use_console)
        filesize = int(cf.get('Mylog','filesize'))

        backupCount = cf.get('Mylog', 'backupCount')
        name = os.path.split(os.path.splitext(sys.argv[0])[0])[-1]
        self.logger = logging.getLogger(name)
        if set_level.lower() == "critical": # 严重错误，表明程序本身可能无法计数运行
            self.logger.setLevel(logging.CRITICAL)
        elif set_level.lower() == "error": # 由于一个比较严重的问题，软件已经不能执行某些功能。
            self.logger.setLevel(logging.ERROR)
        elif set_level.lower() == "warning": # 表示发生了意想不到的事情，或表明在不久的将来发生了一些问题(例如“磁盘空间不足”)。该软件仍按预期工作。
            self.logger.setLevel(logging.WARNING)
        elif set_level.lower() == "info": #确认一切按预期进行。
            self.logger.setLevel(logging.INFO)
        elif set_level.lower() == "debug": #详细信息，通常只有在诊断问题时才感兴趣。
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.NOTSET)

        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_file_path = os.path.join(log_path, ''.join([name,'_',log_name]  ))
        #log_handler = logging.FileHandler(log_file_path, encoding='utf-8')


        log_handler = RotatingFileHandler(log_file_path, maxBytes=filesize*1024*1024,backupCount=backupCount, encoding='utf-8')
        log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s"))
#        print("fdas")

        self.logger.addHandler(log_handler)

        if True:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s"))
            self.logger.addHandler(console_handler)


    def addHandler(self, hdlr):
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, exc_info = True, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)

if __name__ == '__main__':
    loger = logger()
    loger.debug("fdsafdasfdas")
