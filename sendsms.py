#!/usr/local/bin/python3
# -*- coding:utf8 -*-
# 腾讯云短信报警模板(群发模式)
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/')
import time
import logging
import json
from qcloudsms_py import SmsMultiSender
from qcloudsms_py.httpclient import HTTPError

# 配置日志类
sms_log='/tmp/sendsms.log'
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=sms_log, level=logging.DEBUG, format=LOG_FORMAT)

# 短信应用SDK AppID
appid = 2323232  # SDK AppID是1400开头

# 短信应用SDK AppKey
appkey = "sdafsfsfsdfs"

# 需要发送短信的手机号码
# phone_numbers = ["2323269", "2323230"]
phone_numbers = []

# 短信模板ID，需要在短信应用中申请
template_id = 41259  # NOTE: 这里的模板ID`7839`只是一个示例，真实的模板ID需要在短信控制台中申请
# templateId 7839 对应的内容是"您的验证码是: {1}"

# 签名
sms_sign = "zabbix监控"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是一个示例，真实的签名需要在短信控制台申请。

msender = SmsMultiSender(appid, appkey)
#params = ["test1111","test2222"] # 数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
params = []
logging.debug('aaaaaaaaaaaaaa')

try:
	logging.debug("========start开始发送短信===========")
	phone_numbers.append(sys.argv[1])
	#print phone_numbers
	#phone_numbers.extend(list(sys.argv[1]))
	logging.info("              短信接收人是:"+str(phone_numbers))
	report_title=sys.argv[2]
	params.append(report_title)
	logging.info("				 发送标题是:"+report_title)
	report_contents=sys.argv[3]
	logging.info("				 发送内容是:"+report_contents)
	params.append(report_contents)
except Exception as e:
	print(e)
	logging.info("发送失败了,原因如下: ")
	logging.error(str(e))
	#sys.exit(1)

result=''
try:
	result = msender.send_with_param(86, phone_numbers,template_id, params, sign=sms_sign, extend="", ext="")   # 签名参数未提供或者为空时，会使用默认签名发送短信
except HTTPError as e:
	print(e)
	logging.info("发送失败了,原因如下: ")
	logging.error(str(e))
except Exception as e:
	print(e)
	logging.info("       ")
	logging.info("发送失败了,原因如下: ")
	logging.error(str(e))
	#sys.exit(1)
print(result)
logging.info(result)
