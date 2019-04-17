# Ansible Role: redis

规划：
1. 一个master，一个slave节点
2. 通过redis-sentinel进行主备节点监控
3. 通过nutcracker代理，nutcracker同时连接sentinel获取主节点信息，当主节点挂了之后自动连接到新的主节点

运行用户:
root

安装目录：
/usr/local/bin

服务端口：
redis:6379
sentinel:26379
nutcracker:22121

配置文件：
/etc/redis/redis.conf
/etc/redis/sentinel.conf
/etc/nutcracker.yml

PID目录:
/var/run/redis_6379.pid
/var/run/redis-sentinel.pid
/var/run/nutcracker.pid

LOG目录：
/var/log/redis.log
/var/log/redis-sentinel.log
/var/log/nutcracker.log #默认不记录日志

DATA目录：
/data/redis/

Service:
/usr/lib/systemd/system/redis-sentinel.service
/usr/lib/systemd/system/redis-server.service
/usr/lib/systemd/system/nutcracker.service