#!/usr/bin/env python
#  -*- coding:utf-8 -*-

import requests
import json

# 日志配置
import sys
import re
import logging
from util import Readconf
cf = Readconf.Readconf().readConfigFile()
name = cf.get('Mylog','name')
thisfile = sys._getframe().f_code.co_filename
loggername = re.split(r'\\|/|\.',thisfile)[-2]
logger = logging.getLogger(name +'.' + loggername)

from util import tools

class Ctdnotice:
    def ctdnotice_tts(self, serviceName, vccId, messageId, bussinessId, serviceKey, playMode, welcomeIvrName, playMediaName, displayNum, calledNum, mediaContent, numCode, playTime):
        serviceName = serviceName
        messageId = messageId
        vccId = vccId
        displayNum = displayNum
        calledNum = calledNum
        bussinessId = bussinessId
        serviceKey = serviceKey
        playMode = playMode
        welcomeIvrName = welcomeIvrName
        playMediaName = playMediaName
        mediaContent = mediaContent
        numCode = numCode
        playTime = playTime
        values = {
            "header":
                {
                    "serviceName": serviceName,
                    "messageId": messageId,
                    "vccId": vccId
                },
            "body":
                {
                    "displayNum": displayNum,
                    "calledNum": calledNum,
                    "bussinessId": bussinessId,
                    "serviceKey": serviceKey,
                    "playMode": playMode,
                    "welcomeIvrName": welcomeIvrName, # 非必须，欢迎词文件(必须为上传文件的文件名)
                    "playMediaName": playMediaName, # 非必须，验证码前放音文件名
                    "mediaContent": mediaContent, # 非必须，语音通知内容
                    "numCode": numCode, # 非必须，数字验证码
                    "playTime": playTime,
                }
        }

        # 计算mac
        mac = tools.checkMac(values)
        # 透传客户的参数， 这里mac不做计算
        headers = {"Content-type": "application/json"}
        body = json.dumps(values)  # 对数据进行JSON格式化编码
        url = cf.get('ctdnotice', 'url') + mac

        logger.info('url: %s' % url)
        logger.info('body: %s' % body)
        logger.info('headers: %s' % json.dumps(headers))

        req = requests.post(url, data = body, headers = headers)
        return req.text  # 获取服务器返回的页面信息


if (__name__ == '__main__'):
    messageId = "0000000000111111547984564687111"
    vccId = "1007"
    displayNum = "076983705000"
    calledNum = "13810107660"
    bussinessId = "0000001"
    mediaContent = "你好啊朋友这里是测试，谢谢您的配合"
    playTime = "3"
    ctdnotice =Ctdnotice()
    resp = ctdnotice.ctdnotice_tts(vccId, messageId, bussinessId, displayNum, calledNum, mediaContent, playTime)
    print("服务器返回结果：%s" % resp)
