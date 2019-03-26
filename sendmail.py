#!/usr/bin/env python 
# -*- coding:utf8 -*-
# zabbix 邮件报警脚本
# 邮件对象:
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
import smtplib
import sys,os
import time

# 定义邮件服务器信息
from_addr = 'yx@wegooooo.com'
smtpserver = 'smtp.exmail.qq.com'
username = from_addr
password='Yx2016.'


# 参数判断
if len(sys.argv)!=4:
	print "请检查传入参数个数"
	sys.exit(1)
try:
	# 发送给 收件人
	to_addr = sys.argv[1]
	# 邮件标题
	subject = sys.argv[2]
	# 邮件正文
	contents = sys.argv[3]
except Exception,e:
	print e
	sys.exit(1)

msg = MIMEMultipart('alternative')
msg['From'] = Header(u'zabbix的告警机器人 <%s>' %from_addr,'utf-8')
msg['To'] = Header(u'服务器报警消息接收人 <%s>' % to_addr,'utf-8')
msg['Subject'] = Header(subject,'utf-8')
is_ok = """<p style='color:green;'>该告警问题已解决,请知悉!</p>"""
if "OK" not in contents:
	is_ok = """<p style='color:red;'><b>请及时解决该服务器问题!</b></p>"""
mail_msg= """<div style='border:1px solid green;'>
  <h3>zabbix服务器报警信息.</h3>
  <h3>报警时间:&nbsp;&nbsp;"""+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))+"""
  </h3><h4 style='color:green;'>详情请登录地址查看:<a href="http://zabbix.wegooooo.com:1998">zabbix服务器</a></h4>
  <h5>报警详情如下:</h5>
  <p style='color:red;'>""" + contents + """</p><p></p>""" + is_ok
msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))


# 发送邮件
try:
	server = smtplib.SMTP_SSL(smtpserver,port=465)
	#server.set_debuglevel(1)
	server.login(from_addr, password)
	server.sendmail(from_addr, [to_addr], msg.as_string())
	server.quit()
except smtplib.SMTPException,e:
	with open('/tmp/send_email.log','ab+') as f:
		f.write(time.striftime('%Y-%m-%d %H:%M:%S',time.mktime(time.localtime())))
		f.write('\n\r')
		f.write(e)
	print e
