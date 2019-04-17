# Ansible Role: elasticsearch

规划：
1. 默认三个服务器组成集群，可以多个。
2. 默认内存使用服务器的一半，服务器内存超过64G，最多使用32G

运行用户:
elastic

安装目录：
/opt/bigdata/elasticsearch-6.4.3

配置文件：
/opt/bigdata/elasticsearch-6.4.3/config/

PID目录:
/opt/bigdata/elasticsearch-6.4.3/run/elasticsearch.pid

LOG目录：
/opt/bigdata/elasticsearch-6.4.3/logs

DATA目录：
/data/elasticsearch

Service:
/usr/lib/systemd/system/elasticsearch.service