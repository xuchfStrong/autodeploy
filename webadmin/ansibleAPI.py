#!/usr/bin/env python
# coding=utf-8

import os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase


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


class PlayBook(object):
    def __init__(self, subset, tags, HOSTSINVENTORY, PLAYBOOK):
        print("First tags is: %s" % tags)
        if tags is None:
            tags = 'all'
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
        self.inventory = InventoryManager(loader=self.loader, sources=[HOSTSINVENTORY])
        if self.ops.subset != [None]:
            self.inventory.subset(self.ops.subset)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.PLAYBOOK = PLAYBOOK

    def playbookrun(self):

        self.variable_manager.extra_vars = {'customer': 'test', 'disabled': 'yes'}
        playbook = PlaybookExecutor(playbooks=[self.PLAYBOOK],
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader,
                                    options=self.ops,
                                    passwords=self.passwords)
        result = playbook.run()
        if result == 0:
            return "Success"
        else:
            return "Failed"


if __name__ == "__main__":
    a = PlayBook('ambari_server', None)
    a.playbookrun()
