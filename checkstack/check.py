#! /usr/bin/env python

import logging
import sys

from _ceilometer.havana import check_config
from _ceilometer.havana import check_process
from _ceilometer.havana import check_roles

logging.basicConfig(level=logging.INFO)

def check_control():
    check_config.CeilometerControlConfigChecker().check_all()
    check_config.GlanceControlConfigChecker().check_all()
    check_config.CinderControlConfigChecker().check_all()
    check_process.ControlProcessChecker().check()
    check_roles.check_ceilometer_role()

def check_compute():
    check_config.NovaComputeConfigChecker().check_all()
    check_process.ComputeProcessChecker().check()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'control':
        check_control()
    elif len(sys.argv) > 1 and sys.argv[1] == 'compute':
        check_compute()
    else:
        check_control()
        check_compute()
