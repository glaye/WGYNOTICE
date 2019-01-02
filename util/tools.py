import hashlib
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


def getKey(vccId):
    '''
    获取key
    :param vccId:
    :return:
    '''
    # key = md5(vccid + md5(vccid + md5(vccid)))  对vccid的三层md5加密
    # md5加密 hashlib.md5(vccId).hexdigest()
    m1 = hashlib.md5(vccId.encode('utf8')).hexdigest()
    m2 = hashlib.md5((vccId + m1).encode('utf8')).hexdigest()
    key = hashlib.md5((vccId + m2).encode('utf8')).hexdigest()
    logger.debug('vccid : %s , key : %s' % (vccId, key))
    return key

def checkMac(recvBody):
    # 语音通知的key需要转大写
    key = getKey(recvBody['header']['vccId']).upper()
    mac = re.sub('\s*', "", json.dumps(recvBody))
    # mac=md5(md5(json)+key 其中json为请求报文（需要去掉空格，制表符，换行符）
    mac = hashlib.md5((hashlib.md5(mac.encode('utf8')).hexdigest() + key).encode('utf8')).hexdigest()
    return mac


if __name__ == '__main__':
    body = \
        {
            "header":{
                "serviceName":"IVRRequest",
                "messageId":"2222222222",
                "vccId":"10086"
            },
            "body":{
                "displayNum":"100865",
                "calledNum":"13810107660",
                "bussinessId":"2222222222",
                "serviceKey":"900008",
                "playMode":"3",
                "welcomeIvrName":"test",
                "playMediaName":"fdas",
                "mediaContent":"你好,这里是测试，请忽略这个电话",
                "numCode":"abc123",
                "playTime":"3"
            }
        }
    print(type(body))
    print('key : %s' % getKey(body['header']['vccId']))
    import json
    print('mac function : %s' % checkMac(body))


    mac = re.sub(r'\s*', "", json.dumps(body))
    print('mac is %s' % mac)
    # mac=md5(md5(json)+key 其中json为请求报文（需要去掉空格，制表符，换行符）
    mac = hashlib.md5((hashlib.md5(mac.encode('utf8')).hexdigest() + getKey(body['header']['vccId']).upper()).encode('utf8')).hexdigest()
    print('mac : %s' % mac)