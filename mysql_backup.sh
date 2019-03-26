#!/bin/bash
# mysql 数据库备份
hosts=(172.16.0.6 134.175.224.99)
names=(xinceshi_server ceshi_server)
pwds=(truedian#123 truedian#123)
ports=(10011 10011)
mkdir -p /data/backup_dbs
cd /data/backup_dbs

for((i=0;i<${#hosts[@]};i++));do
	mysqldump -A --host=${hosts[$i]} -uroot --password=${pwds[$i]} --port=${ports[$i]} > ${names[$i]}_${hosts[$i]}'_all_'`date +%Y%m%d`.sql
	tar -zcvf ${names[$i]}_${hosts[$i]}'_all_'`date +%Y%m%d_%H_%M_%S`.tar.gz ${names[$i]}_${hosts[$i]}'_all_'`date +%Y%m%d`.sql
	rm -rf ./${names[$i]}_${hosts[$i]}'_all_'`date +%Y%m%d`.sql
	# 保留15天即可
	find ./ -mtime +15 | xargs rm -rf 
done
