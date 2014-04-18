#! /usr/bin/env python

# Copyright (c) 2014, Huawei Technologies Co., Ltd
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#   implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Author: ZhiQiang Fan <aji.zqfan@gmail.com>

import logging
import psutil
import sys

LOG = logging.getLogger(__name__)

class ProcessChecker(object):
    process = {}

    def check(self):
        cmdlines = [p.cmdline for p in psutil.process_iter()]
        for key in self.process:
            found = False
            for cmdline in cmdlines:
                for arg in cmdline:
                    if self.process[key] in arg:
                        found = True
                        break
                if found:
                    break
            if not found:
                LOG.error(self.process[key] + ' not running')

class ControlProcessChecker(ProcessChecker):
    process = {
        'mongo': 'mongod',
        'amqp': 'rabbitmq-server',
        'nova': 'nova-api',
        'keystone':  'keystone-all',
        'glance': 'glance-api',
        'cinder': 'cinder-api',
        'neutron': 'neutron-server',
        'api': 'ceilometer-api',
        'collector': 'ceilometer-collector',
        'central': 'ceilometer-agent-central',
        'evaluator': 'ceilometer-alarm-evaluator',
        'notifier': 'ceilometer-alarm-notifier',
    }

class ComputeProcessChecker(ProcessChecker):
    process = {
        'nova-compute': 'nova-compute',
        'compute': 'ceilometer-agent-compute',
    }

if __name__ == '__main__':
    logging.basicConfig()
    if len(sys.argv) > 1 and sys.argv[1] == 'control':
        ControlProcessChecker().check_process()
    elif len(sys.argv) > 1 and sys.argv[1] == 'compute':
        ComputeProcessChecker().check_process()
    else:
        ControlProcessChecker().check_process()
        ComputeProcessChecker().check_process()
