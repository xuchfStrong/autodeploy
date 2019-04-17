# Ansible Role: mongodb

安装mongodbshard集群，采用三台服务器。
安装完毕后，默认有一个shard：myShard_1
三台服务器上每台都运行mongod-shard,mongod-config,第一台服务器会运行mongos服务，对外提供接口
服务端口分别为：
mongod-config：27019
mongod-shard：27018
mongos：27017

配置文件路径：
/etc/mongod/mongod-config.conf
/etc/mongod/mongod-shard.conf
/etc/mongod/mongos.conf

service路径
/usr/lib/systemd/system/mongod-config.conf
/usr/lib/systemd/system/mongod-shard.conf
/usr/lib/systemd/system/mongos.conf

PID路径：
/var/run/mongodb/mongod-config.pid
/var/run/mongodb/mongod-shard.pid
/var/run/mongodb/mongos.pid

日志路径:
/var/log/mongodb/mongod-config.log
/var/log/mongodb/mongod-shard.log
/var/log/mongodb/mongos.log

DATA路径：
/data/mongo/shard
/data/mongo/config
