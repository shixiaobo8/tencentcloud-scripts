#!/bin/bash
# 使用python2.7 安装supervisor
yum install -y git unzip
which supervisorctl 
if [ $? -eq 0 ];then
	echo "supervisor已经安装完成!"
	supervisorctl status
else
	cd /root/softs/
	#wget -c 'https://codeload.github.com/Supervisor/supervisor/zip/master' -o supervisor-master.zip
	unzip supervisor-master.zip
	cd supervisor-master
	# 确定python 版本
	python2.7 -V
	if [ ! $? -eq 0 ];then
		/bin/bash /data/shell/update_python.sh
		/bin/bash /data/shell/install_pip.sh
	fi
	python setup.py install
	if [ $? -eq 0 ];then
		ln -s /usr/local/bin/supervisor* /usr/bin/
		echo "supervisor 安装完成!,即将配置supervisor"
	fi
	ln -s /usr/local/bin/supervisor* /usr/bin/
	cd /root/soft/
	tar -zxvf supervisor.tar.gz
	#rm -rf /etc/supervisor*
	#mv etc/supervisor* /etc/
	#mv etc/supervisord /etc/init.d/
	chmod +x /etc/init.d/supervisord
	echo "即将修改supervisor 配置文件,加入tomcat"
fi

#supervisord -c /etc/supervisor.conf




