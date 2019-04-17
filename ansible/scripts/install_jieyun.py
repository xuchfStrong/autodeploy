#!/usr/bin/env python
# coding: utf-8

# Description: Get json payload data then trigger an automation deployment
# Author: xuchangfan
# Last modified: 2018-11-26

import os
import sys
import re
import json
import yaml
import ast
import subprocess

PATH_CURRENT = os.path.abspath(__file__)
PATH_PARENT = os.path.dirname(PATH_CURRENT)
WORKHOME = os.path.dirname(PATH_PARENT)
HOSTSINVENTORY = WORKHOME+'/jieyun.hosts'
GROUPVAR = WORKHOME+'/group_vars/all.yml'
PLAYBOOK = WORKHOME+'/jieyun.yml'


def parse_opts():
    """Help messages(-h, --help)."""

    import textwrap
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            '''
            examples:
              {0} -r ambari_server -p "{{'ambari_server':[{{'ip':'192.168.0.51','port':'8080','hostname':'hdp-dev-01.jieyun.com','root_password':'Jieyun2018_com'}}],'repository_server':[{{'ip':'192.168.0.200','hostname':'hdp-05.jieyun.com','port':'80'}}],'database':{{'type':'mysql','users':{{'root':'Jieyun2018_com','ambari':'Jieyun2018_com'}}}}}}"
    
              {0} -r ambari_agent -p "{{'ambari_agent':[{{'ip':'192.168.0.51','hostname':'hdp-dev-01.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.52','hostname':'hdp-dev-02.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.53','hostname':'hdp-dev-03.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.54','hostname':'hdp-dev-04.jieyun.com','root_password':'Jieyun2018_com'}}]}}"
              
              {0} -r elasticsearch -p "{{'elasticsearch':[{{'ip':'192.168.0.51','hostname':'hdp-dev-01.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.52','hostname':'hdp-dev-02.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.53','hostname':'hdp-dev-03.jieyun.com','root_password':'Jieyun2018_com'}}],'repository_server':[{{'ip':'192.168.0.200','hostname':'hdp-05.jieyun.com','port':'80'}}]}}"
              
              {0} -r kibana -p "{{'kibana':[{{'ip':'192.168.0.51','port':'5601','hostname':'hdp-dev-01.jieyun.com','root_password':'Jieyun2018_com'}}]}}"
              
              {0} -r mongodb -p "{{'mongodb':[{{'ip':'192.168.0.51','hostname':'hdp-dev-01.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.52','hostname':'hdp-dev-02.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.53','hostname':'hdp-dev-03.jieyun.com','root_password':'Jieyun2018_com'}}],'repository_server':[{{'ip':'192.168.0.200','hostname':'hdp-05.jieyun.com','port':'80'}}]}}"
              
              {0} -r redis -p "{{'redis':[{{'ip':'192.168.0.51','hostname':'hdp-dev-01.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.52','hostname':'hdp-dev-02.jieyun.com','root_password':'Jieyun2018_com'}},{{'ip':'192.168.0.53','hostname':'hdp-dev-03.jieyun.com','root_password':'Jieyun2018_com'}}],'repository_server':[{{'ip':'192.168.0.200','hostname':'hdp-05.jieyun.com','port':'80'}}]}}"
    
              {0} -v
            '''.format(__file__)
        ))

    exclusion = parser.add_mutually_exclusive_group(required=True)
    exclusion.add_argument('-r', metavar='role', type=str,
                           choices=['ambari_server', 'ambari_agent', 'elasticsearch', 'kibana', 'mongodb', 'redis'],
                           help='role name')
    exclusion.add_argument('-v', action="store_true", help='view the group_vars and hosts inventory')

    parser.add_argument('-p', metavar='payload', type=str, help='payload data json string')

    args = parser.parse_args()
    return {'role': args.r, 'payload': args.p, 'display': args.v}


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


class _AttributeString(str):
    """
    Simple string subclass to allow arbitrary attribute access.
    """

    @property
    def stdout(self):
        return str(self)


def local(cmd, capture=True, shell=None):
    out_stream = subprocess.PIPE
    err_stream = subprocess.PIPE
    p = subprocess.Popen(cmd, shell=True, stdout=out_stream, stderr=err_stream, executable=shell)
    (stdout, stderr) = p.communicate()

    out = _AttributeString(stdout.strip() if stdout else "")
    err = _AttributeString(stderr.strip() if stderr else "")

    out.cmd = cmd
    out.failed = False
    out.return_code = p.returncode
    out.stderr = err
    if out.return_code != 0:
        out.failed = True
    out.succeeded = not out.failed

    return out


def update_ymldata(opts):
    role_name = opts['role']
    payload_json_string = opts['payload']

    with open(GROUPVAR) as f:
        data_dict = yaml.load(f)
        for key_0 in ['ambari_server', 'repository_server', 'database', 'ambari_agent', 'elasticsearch', 'kibana',
                      'kibana', 'mongodb', 'redis']:
            if not data_dict.has_key(key_0):
                data_dict[key_0] = {}

        payload_dict = ast.literal_eval(payload_json_string)

        for key_1 in payload_dict:
            if key_1 in ['ambari_agent', 'elasticsearch', 'kibana', 'mongodb', 'redis', 'ambari_server', 'repository_server']:
                data_dict[key_1] = payload_dict[key_1]
            elif key_1 in []:
                for key_2 in payload_dict[key_1]:
                    data_dict[key_1][key_2] = payload_dict[key_1][key_2]
            elif key_1 in ['database']:
                for key_2 in payload_dict[key_1]:
                    if key_2 == 'type':
                        data_dict[key_1][key_2] = payload_dict[key_1][key_2]
                    elif key_2 == 'users':
                        for key_3 in payload_dict[key_1][key_2]:
                            data_dict[key_1][key_2][key_3] = payload_dict[key_1][key_2][key_3]

    with open(GROUPVAR, 'w') as f:
        yaml.dump(data_dict, f, default_flow_style=False)

    return True


def display_ymldata(opts):
    with open(GROUPVAR) as f:
        data_dict = yaml.load(f)

    print "GROUPVAR: {0}".format(GROUPVAR)
    print json.dumps(data_dict, indent=2)

    return True


def update_inventory(opts):
    role_name = opts['role']
    payload_json_string = opts['payload']

    payload_dict = ast.literal_eval(payload_json_string)

    inventory = InventoryHosts()
    # get ansible inventory hosts objects
    hosts_dict = inventory.load(HOSTSINVENTORY)

    for group_name in []:
        if payload_dict.has_key(group_name):
            inventory_key = '[{0}]'.format(group_name)
            hosts_dict[inventory_key].append(payload_dict[group_name]['ip'])

    for group_name in ['ambari_agent', 'elasticsearch', 'mongodb', 'redis', 'ambari_server', 'kibana']:
        if payload_dict.has_key(group_name):
            inventory_key = '[{0}]'.format(group_name)
            for host_item in payload_dict[group_name]:
                if host_item['ip'] not in hosts_dict[inventory_key]:
                    hosts_dict[inventory_key].append(host_item['ip'])

    # save ansible inventory hosts with new objects
    inventory.save(HOSTSINVENTORY, hosts_dict)

    return True


def display_inventory(opts):
    inventory = InventoryHosts()
    hosts_dict = inventory.load(HOSTSINVENTORY)

    print "HOSTSINVENTORY: {0}".format(HOSTSINVENTORY)
    print json.dumps(hosts_dict, indent=2)

    return True


def run_playbook(opts):
    # empty the ansible.log
    ansible_log = "{0}/log/ansible.log".format(WORKHOME)
    log_file = open(ansible_log, 'w')

    # generate the ansible playbook deploy command
    cmd = """{0}/scripts/ansibleRunner.py {1} -i {2} --limit {3}""".format(WORKHOME, PLAYBOOK, HOSTSINVENTORY,
                                                                           opts['role'])

    # run ansible playbook
    out = local(cmd)
    log_file.write(out)
    log_file.close()
    if "unreachable=0" not in out or "failed=0" not in out:
        return False

    return True


def run_playbook_etc_hosts(opts):
    # record the logs
    ansible_log = "{0}/log/ansible.log".format(WORKHOME)
    log_file = open(ansible_log, 'a')

    # generate the ansible playbook deploy command
    cmd = """{0}/scripts/ansibleRunner.py {1} -i {2} --tags common-etc-ntpd""".format(WORKHOME, PLAYBOOK,
                                                                                      HOSTSINVENTORY)

    # run ansible playbook
    out = local(cmd)
    log_file.write(out)
    log_file.close()
    if "unreachable=0" not in out or "failed=0" not in out:
        return False

    return True


def main():
    if len(sys.argv) < 2:
        os.system(__file__ + " -h")
        return 2

    # locate ansible workhome
    os.chdir(WORKHOME)

    for file_item in [GROUPVAR, HOSTSINVENTORY]:
        if not os.path.isfile(file_item) or os.stat(file_item).st_size == 0:
            print "No such file or with empty size: {0}".format(file_item)
            return 2

    # get parameters
    opts = parse_opts()

    if opts['role'] and opts['payload']:
        # update ansible group_vars
        print "========="
        print "1.1 Updating Ansible GROUP_VARS"
        if update_ymldata(opts):
            print "1.2 OK. Updated Ansible GROUP_VARS successfully"
        else:
            print "1.3 ERROR. Failed to update Ansible GROUP_VARS"

        # update ansible inventory hosts file
        print "========="
        print "2.1 Updating Ansible inventory hosts file"
        if update_inventory(opts):
            print "2.2 OK. Updated Ansible inventory hosts file successfully"
        else:
            print "2.2 ERROR. Failed to updated Ansible inventory hosts file"

        # run ansible playbook with parameter '--limit role_name'
        print "========="
        print "3.1 Running ansible playbook, more details in /var/log/ansible.log"
        if run_playbook(opts):
            print "3.2 OK. Ran ansible playbook successfully"
        else:
            print "3.2 ERROR. Failed to run ansible playbook"
        '''
        # run ansible playbook with parameter '--tags common-etc-ntpd'
        print "========="
        print "4.1 Running ansible playbook to enable the ntp service, more details in /var/log/ansible.log"
        if run_playbook_etc_hosts(opts):
            print "4.2 OK. Ran ansible playbook to enable ntp service successfully"
        else:
            print "4.2 ERROR. Failed to run ansible playbook to enable ntp service"
        '''
    if opts['display']:
        display_ymldata(opts)
        display_inventory(opts)

    return 0


if __name__ == '__main__':
    sys.exit(main())
