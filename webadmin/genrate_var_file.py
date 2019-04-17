#!/usr/bin/python
# _*_ coding: utf8 _*_

import yaml
import sys
import os
from webadmin.models import *

PATH_CURRENT = os.path.abspath(__file__)
PATH_PARENT = os.path.dirname(PATH_CURRENT)
WORKHOME = os.path.dirname(PATH_PARENT)
HOSTSINVENTORY = WORKHOME+'/ansible/jieyun.hosts'
HOSTSINVENTORY_ALLSERVER = WORKHOME+'/ansible/init_server.hosts'
GROUPVAR = WORKHOME+'/ansible/group_vars/all.yml'
GROUPVAR_ALLSERVER = WORKHOME+'/ansible/group_vars/allserver.yml'


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


def match_srv_type(srv_type):
    return {
            'ambari_server': 'ambari',
            'zabbix_server': 'zabbix',
    }.get(srv_type, 'error')    # 'error'为默认返回值，可自设置


# 将主机，repo，database信息生成为dict
def gen_var_dict(task_id):
    host_list = []
    repo_list = []
    db_list = []
    srv_type = Tasks.objects.values_list('srv_type', flat=True).get(task_id=task_id).encode("utf-8")
    host_id = Tasks.objects.values_list('host_id', flat=True).get(task_id=task_id)
    host_id_list = host_id.strip().split(',')
    host_set = Servers.objects.filter(host_id__in=host_id_list).values('ip', 'hostname')
    repo_set = Repository.objects.values('ip', 'port')
    db_set = Databases.objects.filter(srv_type=srv_type).values('srv_type', 'db_type', 'root_password', 'srv_password')

    for i in host_set:
        for k, v in i.items():
            i[k] = v.encode("utf-8")
        host_list.append(i)
    for i in repo_set:
        for k, v in i.items():
            i[k] = v.encode("utf-8")
        repo_list.append(i)
    for i in db_set:
        db_list.append(i)

    if db_list:
        db_type = db_list[0]['db_type'].encode("utf-8")
        root_pwd = db_list[0]['root_password'].encode("utf-8")
        srv_pwd = db_list[0]['srv_password'].encode("utf-8")
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

    dict_combine = {srv_type: host_list, 'repository_server': repo_list, 'database': d1}
    return dict_combine


# 生成所有主机初始化的dict
def gen_var_dict_all_server():
    host_list = []
    host_set = Servers.objects.values('ip', 'hostname', 'root_password')

    for i in host_set:
        for k, v in i.items():
            i[k] = v.encode("utf-8")
        host_list.append(i)

    host_dict = {'servers': host_list}
    return host_dict


# 为生成init_server.hosts生成所有主机初始化的dict
def gen_var_dict_all_server_inventory():
    host_list = []
    host_set = Servers.objects.values('ip', 'hostname', 'root_password')

    for i in host_set:
        for k, v in i.items():
            i[k] = v.encode("utf-8")
        h = ' '.join([ i['ip'], 'hostname='+i['hostname'], 'ansible_connection=ssh', 'ansible_ssh_user=root', 'ansible_ssh_pass='+i['root_password'] ])
        host_list.append(h)

    dict_combine = {'allserver': host_list}
    return dict_combine


def update_inventory(dict):
    inventory = InventoryHosts()
    # get ansible inventory hosts objects
    hosts_dict = inventory.load(HOSTSINVENTORY)
    srv_set = Services.objects.values('service').distinct()
    srv_list = []
    for i in list(srv_set):
        srv_list.append(i['service'].encode('utf-8'))

    for group_name in srv_list:
        if dict.has_key(group_name):
            inventory_key = '[{0}]'.format(group_name)
            for host_item in dict[group_name]:
                if host_item['ip'] not in hosts_dict[inventory_key]:
                    hosts_dict[inventory_key].append(host_item['ip'])

    # save ansible inventory hosts with new objects
    inventory.save(HOSTSINVENTORY, hosts_dict)
    return True


# 生成所有主机的inventory
def update_inventory_all_server(dict):
    inventory = InventoryHosts()
    # get ansible inventory hosts objects
    hosts_dict = inventory.load(HOSTSINVENTORY_ALLSERVER)

    for group_name in ['allserver', 'master', 'slaves']:
        if dict.has_key(group_name):
            inventory_key = '[{0}]'.format(group_name)
            for host_item in dict[group_name]:
                if host_item not in hosts_dict[inventory_key]:
                    hosts_dict[inventory_key].append(host_item)

    # save ansible inventory hosts with new objects
    inventory.save(HOSTSINVENTORY_ALLSERVER, hosts_dict)

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


def genfile_all_server():
    d = gen_var_dict_all_server()
    d2 = gen_var_dict_all_server_inventory()
    if d:
        with open(GROUPVAR_ALLSERVER, 'w+') as f:
            yaml.dump(d, f, default_flow_style=False)
        update_inventory_all_server(d2)
        print("Generate group_var all-server and inventory successful")
        return True
    else:
        return False


if __name__ == '__main__':
    sys.exit(genfile("42"))
    # sys.exit(genfile_all_server())