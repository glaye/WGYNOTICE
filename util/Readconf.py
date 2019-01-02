import configparser
import os
import sys
'''
工具类（读配置文件）
'''
class Readconf:
    # 实例初始化
    def __init__(self):
        # 读取配置文件
        self.cf = self.readConfigFile()

    # 读配置文件
    def readConfigFile(self):
        cf = configparser.ConfigParser()

        path = os.path.join(sys.path[0], '../WGYNOTICE.ini')
        # print path
        cf.read(path)
        return cf