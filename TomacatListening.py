#!/usr/bin/env python
# -*- coding:utf8 -*-
import xlrd,requests,time,smtplib
from email.mime.text import  MIMEText
#读取文件路径
path = "D:\\test\\tomcat.xlsx"
#URL路径
url = "http://ipport/static/index.html?t=1551150161055#/shop_detail/A2017122406393016269"
#超时时间 单位：秒
timeout_time = 10
#轮询时间 单位：秒
poll_time = 120
#邮件配置发送人帐号，密码
sender = "gaojie@wegooooo.com"
passwd = "a12344321A"
#邮件配置接收人
receivers = ["gufenglian@wegooooo.com","linyingjie@wegooooo.com"]
#receivers = ["441805819@qq.com"]

error_ipports = []
ipports =[]
ipportdict={}

def read_excel(path):
    try:
        for i in range(1,xlrd.open_workbook(path).sheet_by_name("Sheet1").nrows):
            ipports.append(xlrd.open_workbook(path).sheet_by_name("Sheet1").cell_value(i,3))
    except Exception as E:
        print(E)

def init_dict():
    for i in ipports:
        ipportdict[i]=0

def listen_tomcat(url):
    time.sleep(poll_time)
    for ipport in ipports:
        try:
            if requests.get(url.replace("ipport",ipport)).elapsed.total_seconds() > timeout_time:
                ipportdict[ipport]+=1
            else:
                ipportdict[ipport]=0
        except Exception as E:
            ipportdict[ipport]+=1

def mail(ipports):
    try:
        msg = MIMEText( "\n".join(ipports))
        msg['From'] = sender
        msg['To'] = ",".join(receivers)
        msg['Subject'] = "访问超时tomcat服务器ip端口"
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com",465)
        server.login(sender,passwd)
        server.sendmail(sender,receivers,msg.as_string())
        server.quit()
    except Exception as E:
        print(E)

if __name__ == '__main__':
    read_excel(path)
    init_dict()
    while True:
        listen_tomcat(url)
        print(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
        for value in  ipportdict:
            if ipportdict[value] > 2:
                error_ipports.append(value)
                print(error_ipports)
                mail(error_ipports)
                ipportdict[value]=0


