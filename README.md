#功能
## 封装CTDNOTICE工程，即语音通知，写死如下信息，其余参数由调用api的客户提交，返回报文本程序返回的是语音通知工程返回的报文，本程序不做处理


url = http://IP:PORT//CTDNOTICE/ICCP?mac=

serviceName = IVRRequest

serviceKey = 900008

playMode = 3

## 日志功能 记录返回报文及客户提交的日志,日志可配置回滚


#生成requirements.txt
pip freeze > requirements.txt

#安装依赖
pip install -r requirements.txt

# 运行
gunicorn -w 50 -b 0.0.0.0:8080 main:app -t 500 -D --access-logfile /data/logs/gunicorn/WGYNOTICE.log
