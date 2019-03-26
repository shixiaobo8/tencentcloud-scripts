#!/bin/bash
# 日志备份 
LOGS_PATH=/data/all_log/nginx_log
LOGS_PATHBK=/data/all_log/nginx_log/logbak
TODAYHOUR=$(date +%Y%m%d%H)
LOGS=(lookbook lookbook_ssl lookbook_wsxc_ssl lookbook_wsxcme_ssl lookbook_wsxcme lookbook_wsxc)
for LOG in ${LOGS[@]}
do
	echo $LOG
	####cut access logs####
	if [ -f ${LOGS_PATH}/access_$LOG.log ];then
		mv ${LOGS_PATH}/access_$LOG.log ${LOGS_PATHBK}/access_$LOG_${TODAYHOUR}.log
	fi

	####cut error logs####
	if [ -f ${LOGS_PATH}/error_$LOG.log ];then
 		mv ${LOGS_PATH}/error_$LOG.log ${LOGS_PATHBK}/error_$LOG_${TODAYHOUR}.log
	fi
done
####reload nginx####
kill -USR1 $(cat /data/all_log/nginx_log/nginx.pid)


####housekeeping logs#####
if [ -d ${LOGS_PATHBK} ]
then
  find ${LOGS_PATHBK}/ -type f -name "*.log" ! -name "*.gz" -exec gzip -9 {} \;
  find ${LOGS_PATHBK}/ -type f -mtime +15 -name "*.gz" -exec rm -f {} \;
  scp -r /data/all_log/nginx_log/logbak/*${TODAYHOUR}.log.gz root@10.135.152.179:/data/nginxlog3
fi
