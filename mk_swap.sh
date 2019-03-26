#!/bin/bash
# 检查系统当前的swap空间大小
swap_size=`free -m  | grep Swap | awk '{print $2}' | awk '{print $1}'` 
echo $swap_size
if [ $swap_size -eq 0 ];then
	mkdir -p /data/swapfiles
	dd if=/dev/zero of=/data/swapfiles/swapfile1 bs=1M count=8096
	mkswap /data/swapfiles/swapfile1
	swapon /data/swapfiles/swapfile1
	echo "/data/swapfiles/swapfile1  swap swap defaults 0 0" >> /etc/fstab
fi
free -m
