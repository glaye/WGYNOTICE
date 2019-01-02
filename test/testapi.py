#!/usr/bin/env python
#  -*- coding:utf-8 -*-
import re
import requests
import json
import hashlib
import uuid

class Ctdnotice:
    def ctdnotice_tts(self, serviceName, vccId, messageId, bussinessId, serviceKey, playMode, welcomeIvrName, playMediaName, displayNum, calledNum, mediaContent, numCode, playTime ):
        serviceName = serviceName
        messageId = messageId
        vccId = vccId
        displayNum = displayNum
        calledNum = calledNum
        bussinessId = bussinessId
        serviceKey = serviceKey
        playMode = playMode
        mediaContent = mediaContent
        playTime = playTime
        welcomeIvrName = welcomeIvrName
        playMediaName = playMediaName
        numCode = numCode
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

        jdata = json.dumps(values)  # 对数据进行JSON格式化编码
        print("提交的报文：%s" % jdata)
        print("加密前的mac：", jdata)
        mac = re.sub('\s*', "", jdata)
        print("替换后的mac：", mac)

        # key = md5(vccid + md5(vccid + md5(vccid)))  对vccid的三层md5加密
        # md5加密 hashlib.md5(vccId).hexdigest()
        m1 = hashlib.md5(vccId.encode('utf8')).hexdigest()
        m2 = hashlib.md5((vccId+m1).encode('utf8')).hexdigest()
        key = hashlib.md5((vccId+m2).encode('utf8')).hexdigest().upper()
        # mac=md5(md5(json)+key 其中json为请求报文（需要去掉空格，制表符，换行符）
        mac = hashlib.md5((hashlib.md5(mac.encode('utf8')).hexdigest() + key).encode('utf8')).hexdigest()
        print("加密后的mac：", mac)
        print("加密后的key：", key)
        url = "http://127.0.0.1:9080/CTDNOTICE/ICCP?mac=" + mac
        headers = {"Content-type": "application/json"}

        req = requests.post(url, data = jdata, headers = headers)
        return req.text  # 获取服务器返回的页面信息


if (__name__ == '__main__'):
    # 1007 的 mac : 62AAF8D552F2660AD23BCED56C2D42D2
    serviceName = "IVRRequest"
    vccId = "10086"
    messageId = str(uuid.uuid1())
    bussinessId = str(uuid.uuid1())
    #messageId = '2222222222'
    #bussinessId = '2222222222'

    serviceKey = "900008"
    # 语音验证码：service_key = 900006
    # 语音通知：servicekey = 900008(70个文字，或放音文件不超24秒)

    playMode = "3"
    # 0：语音验证码语音文件；
    # 2：语音通知语音文件；
    # 3：语音通知TTS合成；

    displayNum = "100865"
    calledNum = "13810107660"

    playTime = "3"
    # 语音播放次数，默认2次。
    # 欢迎词不在重播范围内，所有产品的重播范围为：playMediaName（放音文件）+numCode（验证码）（不超过3次）

# 下面不是必要的参数
    # 欢迎词文件(必须为上传文件的文件名)
    welcomeIvrName = "test"

    playMediaName = "fdas"
    # 验证码前放音文件名
    # 当playMediaName不为空且playMode为 0、2  时（当为2时，文件名不能为空）：播放指定的文件（必须为上传文件的文件名）
    # 格式为8k，16bit

    # 语音通知内容  当playMode为3时：tts播放语音通知内容
    mediaContent = "你好,这里是测试，请忽略这个电话"

    numCode = "abc123"
    # 数字验证码
    # 当playMode为0   时必填且根据字段值读取提前生成好的0 - 9
    # 的数字和26个字母语音文件播放（不使用TTS），当playMode为其他值时为空（不超过10个字符）

    ctdnotice =Ctdnotice()
    resp = ctdnotice.ctdnotice_tts(serviceName, vccId, messageId, bussinessId, serviceKey, playMode, welcomeIvrName, playMediaName, displayNum, calledNum, mediaContent, numCode, playTime )
    print("返回的报文：%s" % resp)