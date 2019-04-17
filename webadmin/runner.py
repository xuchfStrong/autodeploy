#!/usr/bin/python
# _*_ coding: utf8 _*_
import time
import random


def run(srv_type):
    with open(srv_type, 'w+') as f:
        f.write(srv_type)
        f.close()
    time.sleep(6)
    result = random.randint(0, 1)
    if result == 1:
        return 'Success'
    else:
        return 'Failed'


if __name__ == '__main__':
    run('ambari_server')