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

import inspect
import logging
import sys

from oslo.config import cfg

LOG = logging.getLogger(__name__)
ERRORS = 0

#class ConfigCheck(object):
#    def __init__(self, cfg):
#        self.cfg = cfg
#
#    def assert_equal(self, opt, value, group='DEFAULT', level='error'):
#        self.cfg.register_opts([opt], group=group)
#        _value = self.cfg[group][opt.name]
#        if _value != value:
#            msg = ('%s - Expect %s=%s but get %s'
#                   % (self.cfg.project, opt.name, value, _value))
#            self._print_msg(msg, level)
#
#    def _print_msg(self, msg, level):
#        if level.lower() not in ('error', 'warn', 'info'):
#            raise Exception('unrecognized level: %s' % level)
#
#        if level.lower() in ['error']:
#            global ERRORS
#            ERRORS += 1
#            print >> sys.stderr, '    %s - %s' % (level.upper(), msg)
#        else:
#            print '    %s - %s' % (level.upper(), msg)
#
#    def assert_set(self, opt, group='DEFAULT', level='error'):
#        self.cfg.register_opts([opt], group=group)
#        if not self.cfg[group][opt.name]:
#            msg = ('%s - Expect %s is set but not set'
#                   % (self.cfg.project, opt.name))
#            self._print_msg(msg, level)
#
#    def assert_in(self, opt, value, group='DEFAULT', level='error'):
#        self.cfg.register_opts([opt], group=group)
#        _values = self.cfg[group][opt.name]
#        if type(_values) == str:
#            _values = _values.split()
#        if value not in _values:
#            msg = ('%s - Expect %s in %s but not found'
#                   % (self.cfg.project, value, opt.name))
#            self._print_msg(msg, level)

def error(func):
    func.level = 'error'
    return func

def warn(func):
    func.level = 'warn'
    return func

def info(func):
    func.level = 'info'
    return func

def skip(func):
    def _f(*args, **kwargs):
        pass
    return _f

class ConfigChecker(object):
    cli_opts = []
    project = ''

    def __init__(self):
        cfg.CONF = cfg.ConfigOpts()
        self._import()
        cfg.CONF(self.cli_opts, project=self.project)

    def _import(self):
        raise NotImplementedError()

    def assert_equal(self, opt, expected, actual, level='error'):
        if expected != actual:
            msg = 'Expect %s=%s but get %s' % (opt, expected, actual)
            self._log_msg(msg, level)

    def assert_is_set(self, opt, value, level='error'):
        if not value:
            msg = 'Expect %s is set but does not' % opt
            self._log_msg(msg, level)

    def assert_in(self, opt, expected, value, level='error'):
        if expected not in value:
            msg = 'Expect %s in %s but not found' % (expected, opt)
            self._log_msg(msg, level)

    def get_all_checks(self):
        _, methods = zip(*inspect.getmembers(self, inspect.ismethod))
        return filter(lambda m: hasattr(m, 'level'), methods)

    def check_all(self):
        [check() for check in self.get_all_checks()]

    def _log_msg(self, msg, level):
        if level.lower() not in ('error', 'warn', 'info'):
            raise Exception('unrecognized level: %s' % level)

        if level.lower() in ['error']:
            global ERRORS
            ERRORS += 1
        log = getattr(LOG, level)
        log('%s: %s' % (self.project, msg))

class CeilometerControlConfigChecker(ConfigChecker):
    project = 'ceilometer'

    def _import(self):
        # this module registers some cli options, which needs to be registered
        # before the command line and config files are parsed,
        # so it is must imported
        from ceilometer import service

    @error
    def check_connection(self):
        cfg.CONF.import_opt(
            'connection',
            'ceilometer.openstack.common.db.sqlalchemy.session',
            group='database')
        self.assert_is_set('connection', cfg.CONF.database.connection)

    @info
    def check_debug(self):
        cfg.CONF.import_opt('debug', 'ceilometer.openstack.common.log')
        self.assert_equal('debug', True, cfg.CONF.debug, 'info')

    @error
    def check_os_username(self):
        cfg.CONF.import_group('service_credentials', 'ceilometer.service')
        username = cfg.CONF.service_credentials.os_username
        self.assert_is_set('os_username', username)
        self.assert_equal('os_username', 'ceilometer', username, 'warn')

    @error
    def check_os_tenant_name(self):
        cfg.CONF.import_group('service_credentials', 'ceilometer.service')
        tenant_name = cfg.CONF.service_credentials.os_tenant_name
        self.assert_is_set('os_tenant_name', tenant_name)
        self.assert_equal('os_tenant_name', 'service', tenant_name, 'warn')

    @error
    def check_os_password(self):
        cfg.CONF.import_group('service_credentials', 'ceilometer.service')
        password = cfg.CONF.service_credentials.os_password
        self.assert_is_set('os_password', password)

    @error
    def check_admin_user(self):
        cfg.CONF.import_group('keystone_authtoken',
                              'keystoneclient.middleware.auth_token')
        user = cfg.CONF.keystone_authtoken.admin_user
        self.assert_is_set('admin_user', user)
        self.assert_equal('admin_user', 'ceilometer', user, 'warn')

    @error
    def check_admin_tenant_name(self):
        cfg.CONF.import_group('keystone_authtoken',
                              'keystoneclient.middleware.auth_token')
        tenant = cfg.CONF.keystone_authtoken.admin_tenant_name
        self.assert_is_set('admin_tenant_name', tenant)
        self.assert_equal('admin_tenant_name', 'service', tenant, 'warn')

    @error
    def check_admin_password(self):
        cfg.CONF.import_group('keystone_authtoken',
                              'keystoneclient.middleware.auth_token')
        password = cfg.CONF.keystone_authtoken.admin_password
        self.assert_is_set('admin_password', password)

    @warn
    def check_auth_protocol(self):
        cfg.CONF.import_group('keystone_authtoken',
                              'keystoneclient.middleware.auth_token')
        protocol = cfg.CONF.keystone_authtoken.auth_protocol
        self.assert_equal('auth_protocol', 'https', protocol, 'warn')

    @warn
    def check_auth_uri(self):
        cfg.CONF.import_group('keystone_authtoken',
                              'keystoneclient.middleware.auth_token')
        auth_uri = cfg.CONF.keystone_authtoken.auth_uri
        self.assert_is_set('auth_uri', auth_uri, 'warn')


class GlanceControlConfigChecker(ConfigChecker):
    cli_opts = ['--config-file', '/etc/glance/glance-api.conf']
    project = 'glance'

    def _import(self):
        # need to install gettextutil, or it will raise exception when import
        import glance.cmd
        import glance.openstack.common.log
        import glance.notifier

    @error
    def check_rabbit_notification_topic(self):
        cfg.CONF.import_opt('rabbit_notification_topic',
                             'glance.notifier.notify_kombu')
        topic = cfg.CONF.rabbit_notification_topic
        self.assert_equal('rabbit_notification_topic', 'notifications', topic)

    @error
    def check_notifier_strategy(self):
        cfg.CONF.import_opt('notifier_strategy', 'glance.notifier')
        strategy = cfg.CONF.notifier_strategy
        self.assert_equal('notifier_strategy', 'rabbit', strategy)


class NovaComputeConfigChecker(ConfigChecker):
    project = 'nova'

    def _import(self):
        import nova.openstack.common.log

    @error
    def check_instance_usage_audit(self):
        cfg.CONF.import_opt(
            'instance_usage_audit',
            'nova.compute.manager')
        value = cfg.CONF.instance_usage_audit
        self.assert_equal('instance_usage_audit', True, value)

    @error
    def check_instance_usage_audit_period(self):
        cfg.CONF.import_opt(
            'instance_usage_audit_period',
            'nova.utils')
        value = cfg.CONF.instance_usage_audit_period
        self.assert_is_set('instance_usage_audit_period', value)
        self.assert_equal('instance_usage_audit_period',
                          'hour', value, 'info')

    @error
    def check_notify_on_state_change(self):
        cfg.CONF.import_opt(
            'notify_on_state_change',
            'nova.notifications')
        value = cfg.CONF.notify_on_state_change
        self.assert_is_set('notify_on_state_change', value)
        self.assert_equal('notify_on_state_change',
                          'vm_and_task_state', value, 'info')

    @error
    def check_notification_driver(self):
        cfg.CONF.import_opt(
            'notification_driver',
            'nova.openstack.common.notifier.api')
        value = cfg.CONF.notification_driver
        self.assert_equal(
            'notification_driver',
            ['nova.openstack.common.notifier.rpc_notifier',
             'ceilometer.compute.nova_notifier'],
            value)


class CinderControlConfigChecker(ConfigChecker):
    project = 'cinder'

    def _import(self):
        import cinder.openstack.common.log

    @error
    def check_notification_driver(self):
        cfg.CONF.import_opt(
            'notification_driver',
            'cinder.openstack.common.notifier.api')
        value = cfg.CONF.notification_driver
        self.assert_equal(
            'notification_driver',
            ['cinder.openstack.common.notifier.rpc_notifier'],
            value)

class SwiftControlConfigChecker(ConfigChecker):
    project = 'swift'
    cli_opts = ['--config-file', '/etc/swift/proxy-server.conf']

    def _import(self):
        pass

    @error
    def check_ceilometer_filter(self):
        pass

#def check_swift_control():
#    cfg.CONF(['--config-file', '/etc/swift/proxy-server.conf'],
#             project='swift')
#    c = ConfigCheck(cfg.CONF)
#    c.assert_equal(cfg.StrOpt('use'), 'egg:ceilometer#swift',
#                   'filter:ceilometer')
#    c.assert_in(cfg.StrOpt('pipeline'), 'ceilometer', 'pipeline:main')

