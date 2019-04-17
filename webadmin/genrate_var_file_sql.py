#!/usr/bin/python
# _*_ coding: utf8 _*_

import sqlite3
import yaml
import sys
import os


PATH_CURRENT = os.path.abspath(__file__)
PATH_PARENT = os.path.dirname(PATH_CURRENT)
WORKHOME = os.path.dirname(PATH_PARENT)
HOSTSINVENTORY = WORKHOME+'/ansible/jieyun.hosts'
GROUPVAR = WORKHOME+'/ansible/group_vars/all.yml'
PLAYBOOK = WORKHOME+'/ansible/jieyun.yml'
DBPATH = WORKHOME+'/db.sqlite3'


class InventoryHosts(object):
    def __init__(self):
        object.__init__(self)

    def _writes(self, filename, content):
        assert len(content) > 0, "write content is empty"
        with open(filename, 'wb') as f:
            f.write(content)
            f.close()

    def _read(self, filename):
        with open(filename) as file:
            result = list()
            for line in file.readlines():
                line = line.strip()
                if not len(line) or line.startswith('#'):
                    continue
                result.append(line)
            return result

    def _build(self, lines):
        objs = dict()
        # key = ''
        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                if not objs.has_key(line):
                    objs[line] = list()
                # key = line
                # continue
            # objs[key].append(line)
        return objs

    def load(self, filename):
        lines = self._read(filename)
        objs = self._build(lines)
        return objs

    def save(self, filename, objs):
        content = ''
        for (k, v) in objs.items():
            name = k
            value = '\n'.join(v)
            content = '{0}\n{1}\n{2}\n'.format(content, name, value)
        self._writes(filename, content)


def gen_server_list(list, tuple):
    result_list = []
    for row in tuple:
        result = dict()
        result[list[0]] = str(row[0])  # 将row中的每个元素，追加到字典中。　
        result[list[1]] = str(row[1])
        result[list[2]] = str(row[2])
        result[list[3]] = str(row[3])

        result_list.append(result)
    return result_list


def gen_repo_list(list, tuple):
    result_list = []
    for row in tuple:
        result = dict()
        result[list[0]] = str(row[0])  # 将row中的每个元素，追加到字典中。　
        result[list[1]] = str(row[1])

        result_list.append(result)
    return result_list


def match_srv_type(srv_type):
    return {
            'ambari_server': 'ambari',
            'zabbix_server': 'zabbix',
    }.get(srv_type, 'error')    # 'error'为默认返回值，可自设置


def gen_var_dict(srv_type):
        srv_list = []
    # try:
        # 查询安装的server的信息
        conn = sqlite3.connect(DBPATH)
        cursor = conn.cursor()
        sql_srv = "SELECT srv_type,ip,hostname,port  from webadmin_hosts WHERE srv_type='%s'" % srv_type
        dict_srv = cursor.execute(sql_srv)
        tuple_srv = dict_srv.fetchall()  # 转换为元组
        conn.close()

        if tuple_srv:
            fields_srv = dict_srv.description  # 获取查询结果中列的字段名，如果查询SQL中使用别名，此处显示别名。
            # 将列名加入数据中
            column_list_srv = []
            for i in fields_srv:
                column_list_srv.append(i[0])
            srv_list = gen_server_list(column_list_srv, tuple_srv)
        else:
            print("查询%s 的HOST信息失败" % srv_type)

        # 查询repository_server
        conn_repo = sqlite3.connect(DBPATH)
        cursor_repo = conn_repo.cursor()
        sql_repo = "SELECT ip,port from webadmin_repository"
        dict_repo = cursor_repo.execute(sql_repo)
        tuple_repo = dict_repo.fetchall()
        conn_repo.close()

        if tuple_repo:
            fields_repo = dict_repo.description
            # 将列名加入数据中
            column_list_repo = []
            for i in fields_repo:
                column_list_repo.append(i[0])
            repo_list = gen_repo_list(column_list_repo, tuple_repo)
        else:
            print("查询yum源信息失败")

        # 查询database
        conn_db = sqlite3.connect(DBPATH)
        cursor_db = conn_db.cursor()
        sql_db = "SELECT srv_type,db_type,root_password,srv_password from webadmin_databases WHERE srv_type='%s'" % srv_type
        dict_db = cursor_db.execute(sql_db)
        tuple_db = dict_db.fetchall()
        conn_db.close()

        if tuple_db:
            db_type = tuple_db[0][1].encode("utf-8")
            root_pwd = tuple_db[0][2].encode("utf-8")
            srv_pwd = tuple_db[0][3].encode("utf-8")
        else:
            db_type = None
            root_pwd = None
            srv_pwd = None

        d = {}
        d1 = d.setdefault('database', {})
        d2 = d1.setdefault('users', {})
        d1.setdefault('type', db_type)
        d2.setdefault(match_srv_type(srv_type), srv_pwd)
        d2.setdefault('root', root_pwd)

        dict_combine = {srv_type: srv_list, 'repository_server': repo_list, 'database': d1}
        return dict_combine

    # except:
    #    print("查询数据库失败")
    #    return False


def update_inventory(dict):
    inventory = InventoryHosts()
    # get ansible inventory hosts objects
    hosts_dict = inventory.load(HOSTSINVENTORY)

    for group_name in ['ambari_agent', 'elasticsearch', 'mongodb', 'redis', 'ambari_server', 'kibana']:
        if dict.has_key(group_name):
            inventory_key = '[{0}]'.format(group_name)
            for host_item in dict[group_name]:
                if host_item['ip'] not in hosts_dict[inventory_key]:
                    hosts_dict[inventory_key].append(host_item['ip'])

    # save ansible inventory hosts with new objects
    inventory.save(HOSTSINVENTORY, hosts_dict)

    return True


def genfile(srv_type):
    d = gen_var_dict(srv_type)
    if d:
        with open(GROUPVAR, 'w+') as f:
            yaml.dump(d, f, default_flow_style=False)
        update_inventory(d)
        print("Generate group_var and inventory successful")
        return True
    else:
        return False


if __name__ == '__main__':
    sys.exit(genfile("ambari_server"))