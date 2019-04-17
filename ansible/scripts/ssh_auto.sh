#!/bin/bash

#------------------------------------------#
# FileName:             ssh_auto.sh
# Revision:             1.1.0
# Date:                 2018-11-19 09:50:33
# Description:          This script can achieve ssh password-free login, 
#                       and can be deployed in batches, configuration
#------------------------------------------#

# 读取host文件内容，设置/etc/hosts
echo "127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4" >  /etc/hosts
echo "::1         localhost localhost.localdomain localhost6 localhost6.localdomain6" >> /etc/hosts
while read line;do
        host_type=`echo $line | sed s/[[:space:]]//g | cut -d "," -f1`     # 提取文件中的服务器类型
        host_name=`echo $line | sed s/[[:space:]]//g | cut -d "," -f2`     # 提取文件中的主机名
        ip=`echo $line | sed s/[[:space:]]//g |cut -d "," -f3`             # 提取文件中的ip
        user_name=`echo $line | sed s/[[:space:]]//g |cut -d "," -f4`      # 提取文件中的用户名
        pass_word=`echo $line | sed s/[[:space:]]//g |cut -d "," -f5`      # 提取文件中的密码
		
        if [ ! -z $ip ] ; then	
            printf "=========\n"
            printf "添加$ip-$host_name到/etc/hosts中\n"
            echo "$ip  $host_name" >> /etc/hosts
        fi
done < host_ip.txt      # 读取存储ip的文件


# 密钥对不存在则创建密钥
if [ ! -f ~/.ssh/id_rsa.pub ] ; then  
	ssh-keygen  -t rsa -P '' -f ~/.ssh/id_rsa 1>/dev/null 2>&1
else
	rm -rf ~/.ssh/
	ssh-keygen  -t rsa -P '' -f ~/.ssh/id_rsa 1>/dev/null 2>&1
fi


# 读取host文件内容，循环设置服务器
while read line;do
        host_type=`echo $line | sed s/[[:space:]]//g | cut -d "," -f1`     # 提取文件中的服务器类型
        host_name=`echo $line | sed s/[[:space:]]//g | cut -d "," -f2`     # 提取文件中的主机名
        ip=`echo $line | sed s/[[:space:]]//g |cut -d "," -f3`             # 提取文件中的ip
        user_name=`echo $line | sed s/[[:space:]]//g |cut -d "," -f4`      # 提取文件中的用户名
        pass_word=`echo $line | sed s/[[:space:]]//g |cut -d "," -f5`      # 提取文件中的密码


#将密钥拷贝到其他机器
if [ ! -z $ip ] ; then
printf "=========\n"
printf "配置服务器$ip的ssh密钥\n"
/usr/bin/expect <<-EOF
set timeout 30
spawn ssh-copy-id $user_name@$ip
expect {
"*yes/no" { send "yes\n"; exp_continue }
"*password:" { send "$pass_word\n" }
}
spawn ssh $user_name@$host_name date
expect {
"*yes/no" { send "yes\n"; exp_continue }
"*password:" { send "$pass_word\n" }
}
expect eof
EOF

    if [ $host_type == "agent" ] ; then
	    ssh -n $ip "ssh-keygen  -t rsa -P '' -f ~/.ssh/id_rsa 1>/dev/null 2>&1"
    fi

    #将所有服务器的公钥存入server的authorized_keys中
	    ssh -n $ip 'cat ~/.ssh/id_rsa.pub' >> ~/.ssh/authorized_keys
fi  
done < host_ip.txt      # 读取存储ip的文件



# 将所有authorized_keys,known_hosts和hosts分发到各服务器，并修改主机名
while read line;do
        host_type=`echo $line | sed s/[[:space:]]//g | cut -d "," -f1`     # 提取文件中的服务器类型
        host_name=`echo $line | sed s/[[:space:]]//g | cut -d "," -f2`     # 提取文件中的主机名
        ip=`echo $line | sed s/[[:space:]]//g |cut -d "," -f3`             # 提取文件中的ip
        user_name=`echo $line | sed s/[[:space:]]//g |cut -d "," -f4`      # 提取文件中的用户名
        pass_word=`echo $line | sed s/[[:space:]]//g |cut -d "," -f5`      # 提取文件中的密码
		
	#修改主机名
	if [ ! -z $ip ] ; then
        ssh -n $user_name@$ip "hostnamectl  set-hostname $host_name"		
        printf "=========\n"
        printf "给服务器$ip分发authorized_keys、known_hosts和hosts\n"
        scp  ~/.ssh/authorized_keys $user_name@$ip:~/.ssh/
        scp  ~/.ssh/known_hosts $user_name@$ip:~/.ssh/
        scp  /etc/hosts $user_name@$ip:/etc/hosts
	fi
  
done < host_ip.txt      # 读取存储ip的文件
