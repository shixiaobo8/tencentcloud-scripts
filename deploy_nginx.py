#!/usr/bin/python
# -*- coding:utf8 -*-
# 定义一组写死的组ip
import sys,os
import commands

# nginx 组配置
group_servers = {
	'g1':['xc2server','xc4server','xc7server','xc27server'],
	'g2':['xc8server','xc26server','xc25server','xc39server'],
	'g3':['xc34server','xc35server','xc36server','xc38server'],
	'g4':['xc23server','xc24server','xc30server','xc33server','xc37server'],
	'g5':['xc28server','xc29server','xc31server','xc32server'],
	'g6':['xc40server','xc42server','xc43server','xc46server'],
	'g7':['xc44server','xc45server','xc47server','xc48server']
}

# nginx server 配置路径 
nginx_server_dir = '/usr/local/nginx/conf/server'
# nginx配置文件名称
ng_server_confs = ['szwego.com.conf','wsxcme.com.conf','wsxc.me.conf']
# 全局组变量
group = ''
# 全局功能变量
fun = ''

# 命令行参数
if len(sys.argv) != 3:
	print('\033[0m')
	print("\033[7;31m errror,请按顺序传入两个必要参数 '1:server组' '2添加注释请填写add，取消注释请填写cancel',\033[1;31;31m")
	print("\033[7;33m 		例如: python deploy_nginx.py g1 add \033[1;31;33m")
	print('\033[0m')
	sys.exit(1)

# 检查组参数
try:
	group = sys.argv[1]
	servers = group_servers[group]
except Exception,e:
	print "传入的组不存在!"
	sys.exit(1)

# 检查取消或者添加注释参数
try:
	fun = sys.argv[2]
	if fun != 'add' and fun != 'cancel':
		print("\033[7;31m errror, 参数2必须是 add 或者 cancel',\033[1;31;31m")
		print("\033[7;33m 		例如: python deploy_nginx.py g1 add \033[1;31;33m")
except Exception,e:
	print "添加或者取消注释参数错误!"
	sys.exit(1)

# 逐个配置文件匹配
for server in servers:
	for conf in ng_server_confs:
		conf = nginx_server_dir + os.sep + conf
		# 先匹配行号
		cmd = "grep  -n " + server + " " + conf
		crs = commands.getstatusoutput(cmd)
		line = ''
		if crs[0] == 0:
			lines = crs[1].split('\n')
			for line in lines:
				line = line.split(":")[0]
				# 检查该行是否已被注释
				is_comments = commands.getstatusoutput("sed -n '" + str(line) + "p' " + conf)[1].startswith('#')
				if fun == 'add':
					# 行首有注释不需要添加注释
					if is_comments:
						pass
					else:
						# 添加注释
						add_cmd = "sed -i '" + str(line) + "s/^/#/' " + conf
						# 行首无注释添加注释
						ars = commands.getstatusoutput(add_cmd)[0]
					print conf + " " + server  + " 第" + str(line) + "行成功添加注释!"
				if fun == 'cancel':
					if is_comments:
						# 行首注释,则取消注释
						cancel_cmd = "sed -i '" + str(line) + "s/^#//' " + conf
						cancel_rs = commands.getstatusoutput(cancel_cmd)[0]
					else:
						# 行首无注释,则不用管
						pass
					print  conf + " " + server  + " 第" + str(line) + "行取消注释成功!"

# 配置完成,重启服务
reload_cmd = '/usr/local/nginx/sbin/nginx -s reload'
rrs = commands.getstatusoutput(reload_cmd)[0]
if rrs == 0:
	print "服务启动成功!"
else:
	print "服务启动失败,请检查参数!"
