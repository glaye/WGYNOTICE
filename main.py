#!/usr/bin/env python
#  -*- coding:utf-8 -*-
from flask import Flask
from flask import request
from flask import jsonify

import os
import sys
import json
import re

import logging
from logging.handlers import RotatingFileHandler

from util import Ctdnotice, Myrediscluster
from util import Readconf
from util import tools

# 配置对象
cf = Readconf.Readconf().readConfigFile()

# 全局日志设置
name = cf.get('Mylog', 'name')
set_level = cf.get('Mylog', 'set_level')
log_path = os.path.join(cf.get('Mylog', 'log_path'), "logs")
if sys.platform == 'win32': log_path = os.path.dirname(os.path.realpath(__file__))
filesize = int(cf.get('Mylog', 'filesize'))
backupCount = cf.get('Mylog', 'backupCount')

logger = logging.getLogger(name)
if set_level.lower() == "critical":  # 严重错误，表明程序本身可能无法计数运行
    logger.setLevel(logging.CRITICAL)
elif set_level.lower() == "error":  # 由于一个比较严重的问题，软件已经不能执行某些功能。
    logger.setLevel(logging.ERROR)
elif set_level.lower() == "warning":  # 表示发生了意想不到的事情，或表明在不久的将来发生了一些问题(例如“磁盘空间不足”)。该软件仍按预期工作。
    logger.setLevel(logging.WARNING)
elif set_level.lower() == "info":  # 确认一切按预期进行。
    logger.setLevel(logging.INFO)
elif set_level.lower() == "debug":  # 详细信息，通常只有在诊断问题时才感兴趣。
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.NOTSET)

if not os.path.exists(log_path):
    os.makedirs(log_path)
log_file_path = os.path.join(log_path, name)
log_handler = RotatingFileHandler(log_file_path, maxBytes=filesize * 1024 * 1024, backupCount=backupCount,
                                  encoding='utf-8')
log_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s"))
logger.addHandler(log_handler)
if True:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s:%(lineno)d %(message)s"))
    logger.addHandler(console_handler)

# redis群集连接对象
rc = Myrediscluster.Myrediscluster()

# flask对象
app = Flask(__name__)

@app.route('/CTDNOTICE/ICCP', methods=['POST','GET'])
def process():
    # 接收 mac 和 报文
    mac = request.args.get("mac")
    recvBody = request.get_json(force=True)

    # 判断vccid是否为测试用的
    if (recvBody['header']['vccId'] == '1007') and (not mac == '62AAF8D552F2660AD23BCED56C2D42D2'):
        rtn = {"body":{"result":"0001","reason":"vccId is Illegal!"},"header":{"serviceName":"IVRResponse","messageId":recvBody['header']['messageId']}}
        logger.debug(rtn)
        return jsonify(rtn)

    # 判断 vccid是否合法，是否有对应分配的主叫号码
    displayNum = rc.get(recvBody['header']['vccId'])  # 拿vccid去redis里取主叫，vccid固定主叫
    if displayNum == 'None' or displayNum is None:
        rtn = {"body":{"result":"0001","reason":"vccId is Illegal!"},"header":{"serviceName":"IVRResponse","messageId":recvBody['header']['messageId']}}
        logger.debug(rtn)
        return jsonify(rtn)

    # 判断mac是否正确
    token = tools.checkMac(recvBody)
    logger.debug('token : %s , mac : %s' % (token, mac))
    if ( mac != token):
        rtn = {"body":{"result":"0001","reason":"mac is error!"},"header":{"serviceName":"IVRResponse","messageId":recvBody['header']['messageId']}}
        logger.debug(rtn)
        return jsonify(rtn)

    logger.debug("client_post: %s" % recvBody)


    serviceName = recvBody['header']['serviceName']
    vccId = recvBody['header']['vccId']
    messageId = recvBody['header']['messageId']
    bussinessId = recvBody['body']['bussinessId']
    serviceKey = recvBody['body']['serviceKey']
    playMode = recvBody['body']['playMode']
    calledNum = recvBody['body']['calledNum']
    playTime = recvBody['body']['playTime']

    welcomeIvrName = recvBody['body']['welcomeIvrName']  if 'welcomeIvrName' in recvBody['body'] else None
    playMediaName = recvBody['body']['playMediaName'] if 'playMediaName' in recvBody['body'] else None
    mediaContent = recvBody['body']['mediaContent']  if 'mediaContent' in recvBody['body'] else None
    numCode = recvBody['body']['numCode']  if 'numCode' in recvBody['body'] else None

    ctdnotic = Ctdnotice.Ctdnotice()
    resp = ctdnotic.ctdnotice_tts(serviceName, vccId, messageId, bussinessId, serviceKey, playMode, welcomeIvrName, playMediaName, displayNum, calledNum, mediaContent, numCode, playTime)
    logger.debug("ctdnotice_resp：%s" % resp)
    return jsonify(json.loads(resp))

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    config = dict(
        debug=True,
        host='127.0.0.1',
        port=8080,
        #port=9080,
    )
    app.run(**config)
