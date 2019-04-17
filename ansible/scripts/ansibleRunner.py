#!/usr/bin/env python

import os
import sys
 
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
import ansible.constants as C

def parse_opts():
    """Help messages(-h, --help)."""

    import textwrap
    import argparse

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
        '''
        examples:
          {0} jieyun.yml -i jieyun.hosts --tags common --limit hdp-cloud-01.jieyundata.com
        '''.format(__file__)
        ))

    parser.add_argument('playbook', action="store", type=str)
    parser.add_argument('-i', metavar='inventory', type=str, required=True, help='the inventory hosts file')
    parser.add_argument('--tags', metavar='tag', type=str, help='the tag name')
    parser.add_argument('--limit', metavar='subset', type=str, help='the subset host or group')
    args = parser.parse_args()

    return {'playbook':args.playbook, 'inventory_file':args.i, 'tags':args.tags, 'subset':args.limit}
 
 
class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        # super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
 
    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result
 
    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result
 
    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result
 
 
class AnsibleApi(object):
    def __init__(self, playbook, hosts=None,subset=None,tags=None):
        print "First tags is: %s" %tags
        if tags is None:
           tags='all'
        self.Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo',
                              'diff',
							  'subset',
							  'tags'])
        
        self.ops = self.Options(connection='smart',
                              remote_user=None,
                              ack_pass=None,
                              sudo_user=None,
                              forks=5,
                              sudo=None,
                              ask_sudo_pass=False,
                              verbosity=5,
                              module_path=None,
                              become=None,
                              become_method=None,
                              become_user=None,
                              check=False,
                              diff=False,
                              listhosts=None,
                              listtasks=None,
                              listtags=None,
                              syntax=None,
							  subset=[subset],
							  tags=[tags])
 
        self.loader = DataLoader()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        self.inventory = InventoryManager(loader=self.loader, sources=[hosts])
        if self.ops.subset != [None]:
           self.inventory.subset(self.ops.subset)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        print "Tags is %s:"%self.ops.tags
		
		# setup playbook executor, but don't run until run() called
        self.pbex = PlaybookExecutor(
            playbooks=[playbook],
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            options=self.ops,
            passwords=self.passwords)

    def run(self):
        # run playbook and get stats
        self.pbex.run()
        stats = self.pbex._tqm._stats

        return stats
 
    def runansible(self,host_list, task_list):
 
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
 
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
                passwords=self.passwords,
                stdout_callback=self.results_callback,
                run_additional_callbacks=C.DEFAULT_LOAD_CALLBACK_PLUGINS,
                run_tree=False,
            )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)
 
        results_raw = {}
        results_raw['success'] = {}
        results_raw['failed'] = {}
        results_raw['unreachable'] = {}
 
        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)
 
        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']
 
        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']
 
        print results_raw
 
	"""
    def playbookrun(self, playbook_path):
 
        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, options=self.ops, passwords=self.passwords)
        result = playbook.run()
        return result
	"""

def main():
    if len(sys.argv) < 2:
        os.system(__file__ + ' -h')
        return 2

    # locate ansible workhome
    # os.chdir(WORKHOME)

    # get parameters
    opts = parse_opts()
    
    # run ansible playbook
    runner = AnsibleApi(
        playbook=opts['playbook'],
        hosts=opts['inventory_file'],
		tags=opts['tags'],
		subset=opts['subset']
    )

    stats = runner.run()
    return 0
    #return stats
	
if __name__ == "__main__":
	main()
	"""
    a = AnsibleApi()
    host_list = ['192.168.0.52']
    tasks_list = [
        dict(action=dict(module='command', args='ls')),
        # dict(action=dict(module='shell', args='python sleep.py')),
        # dict(action=dict(module='synchronize', args='src=/home/op/test dest=/home/op/ delete=yes')),
    ]
    a.runansible(host_list,tasks_list)
    a.playbookrun(playbook_path=['/etc/ansible/test.yml'])
	"""
