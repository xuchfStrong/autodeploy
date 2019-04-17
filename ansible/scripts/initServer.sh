#!/bin/bash

logFile="../log/ssh_auto.log"
rm -rf $logFile 
touch $logFile
printf "=======\n"
printf "Start the initialization, more details please check in /opt/ansible/log/ssh_auto.log\n"
#Install expect
printf "=======\n"
printf "Install expect...\n"
echo "Install expect..." > $logFile
yum install expect -y >> $logFile

#Install ansible
printf "=======\n"
printf "Install ansible...\n"
echo "" >> $logFile
echo "Install ansible..." >> $logFile
yum -y install ansible >> $logFile

#服务器环境初始化

printf "=======\n"
echo "" >> $logFile
echo "Start to init the hosts..." >> $logFile
printf "Start to init the servers...\n"
sh ssh_auto.sh >> $logFile
printf "=======\n"
printf "Server initialization completed\n"
echo "" >> $logFile
echo "Server initialization completed" >> $logFile
printf "\n"
