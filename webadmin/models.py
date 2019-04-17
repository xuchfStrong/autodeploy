# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


# 用户
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


# 全部主机
class Servers(models.Model):
    host_id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    hostname = models.CharField(max_length=50)
    root_password = models.CharField(max_length=50)
    host_type = models.CharField(max_length=50, default='servers')


# 初始化服务器状态
class InitServer(models.Model):
    id = models.AutoField(primary_key=True)
    server_list = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default=None, null=True)


# 主机
class Hosts(models.Model):
    host_id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    hostname = models.CharField(max_length=50)
    srv_type = models.CharField(max_length=50)

    def __str__(self):
        return self.hostname


# yum仓库
class Repository(models.Model):
    repo_id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=50)
    port = models.CharField(max_length=10)


# 数据库
class Databases(models.Model):
    db_id = models.AutoField(primary_key=True)
    srv_type = models.CharField(max_length=50)
    db_type = models.CharField(max_length=20)
    root_password = models.CharField(max_length=20)
    srv_password = models.CharField(max_length=20)


# 任务
class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    srv_type = models.CharField(max_length=50)
    host_list = models.CharField(max_length=500)
    host_id = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now_add=True)
    task_status = models.CharField(max_length=50, default='NewTask')


# 安装业务类型
class Services(models.Model):
    service = models.CharField(max_length=50)
    is_db = models.BooleanField(default=False)
    db_type = models.CharField(max_length=20, null=True)




