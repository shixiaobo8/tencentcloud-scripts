#!/bin/bash
# 自动化创建用户脚本,包括:  1.创建用户家目录 2.创建用户密码 3.初始化.bash_profile和vimrc 4.初始化ssh登录密钥

#  获取用户名称
username=$1
if [ $# -eq 0 ];then
	echo -e "\033[33m ERR:缺少用户名参数 \033[0m"
	echo -e "\033[32m　使用方式:\033[0m"
	echo -e "\033[32m	 sh automakeuser.sh bobo(用户名) \033[0m"
	exit 0
fi

main(){
	create_user
	echo "如果批量创建用户的服务器比较多因为涉及到权限的修改,所有会比较慢,请耐心等待该程序执行完毕!"
	get_tomcat_dirs
	init_userEnv
	init_userSshKey
}

# 创建用户并设置密码
create_user(){
	groupadd developers
	useradd -g developers $username
	user_passwd=`date +%Y%m%d`"@"$username
	echo $user_passwd | passwd $username --stdin
	echo "用户创建成功,即将初始化用户数据!"
}

# 初始化用户环境变量
init_userEnv(){
	# 别名设置
	cp -rp /root/.bash_profile  /home/$username/.bash_profile
	chown $username:developers /home/$username/.bash_profile
	cp  -rp /root/.vimrc  /home/$username/.vimrc
	chown $username:developers /home/$username/.vimrc
}

# tomcat 获取机器的tomcat 目录并设置权限
get_tomcat_dirs(){
	# 公网ip 取ip的最后一个尾数
	public_ipv4=`curl -s http://metadata.tencentyun.com/meta-data/public-ipv4`
	ip_tail=`echo  $public_ipv4 | awk -F"."  '{print $4}'`
	tomcats=(/data/tomcat/business_tomcat_${ip_tail}_web_1 /data/tomcat/business_tomcat_${ip_tail}_web_2 /data/tomcat/business_tomcat_${ip_tail}_web_3 /data/tomcat/business_tomcat_${ip_tail}_web_4)

	for tomcat in ${tomcats[@]}
	do
		chgrp -R developers $tomcat
		if [ -d $tomcat ];then
			list_alldir $tomcat
		fi
	done

}

# 初始化用户SSH 密钥
init_userSshKey(){
	echo yes | sudo -u $username ssh-keygen -t rsa -f /home/$username/.ssh/id_rsa.pub -N '' -b 1024
	#echo -n "请输入ssh密钥:"
	#read key
	# echo $key >> /home/$username/.ssh/authorized_keys
	echo "ssh-key 已生成,管理员请及时添加服务器用户key!,多服务器请在ansible端执行!"
}	

# 给目录和文件分别设置权限
list_alldir(){  
	for file2 in `ls -a $1`  
	do  
		if [ x"$file2" != x"." -a x"$file2" != x".." ];then  
			if [ -d "$1/$file2" ];then  
					#echo "是一个目录,正在修改目录权限"
				    chmod g+r,o+x   "$1/$file2"  
					list_alldir "$1/$file2"  
			fi
			if [ -f "$1/$file2" ];then  
					#echo "正在修改$1/$file2的文件权限"
				    chmod o+r  "$1/$file2"  
			fi
		fi  
	done  
}  


main

