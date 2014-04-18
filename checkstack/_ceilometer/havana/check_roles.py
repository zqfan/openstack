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

import os
from keystoneclient.v2_0 import client

def get_os_env(env):
    value = os.environ.get(env)
    if not value:
        raise SystemExit('[ERROR] Require %s but not found in os '
                         'environment, please export it' % env)
    return value

def get_keystone_client():
    user_name = get_os_env('OS_USERNAME')
    tenant_name = get_os_env('OS_TENANT_NAME')
    password = get_os_env('OS_PASSWORD')
    auth_url = get_os_env('OS_AUTH_URL')

    if user_name != 'admin' or tenant_name != 'admin':
        raise SystemExit('[ERROR] Require admin authorization '
                         'but not satisfied')

    return client.Client(username=user_name,
                         tenant_name=tenant_name,
                         password=password,
                         auth_url=auth_url)

def get_ceilometer_user_id(ksclient):
    users = ksclient.users.list()
    for user in users:
        if user.name == 'ceilometer':
            return user.id

    raise SystemExit('[ERROR] Requires ceilometer user but not found. '
                     'Use keystone user-create to add it')

def get_service_tenant_id(ksclient):
    tenants = ksclient.tenants.list()
    for tenant in tenants:
        if tenant.name == 'service':
            return tenant.id

    raise SystemExit('[ERROR] Requires service tenant but not found. '
                     'Use keystone tenant-create to add it')

def check_keystone_roles(ksclient):
    """kesytone should create 'admin' and 'ResellerAdmin' role."""
    roles = ksclient.roles.list()
    role_names = map(lambda role: role.name, roles)
    if 'admin' not in role_names:
        raise SystemExit('[ERROR] Keystone should create "admin" role '
                         'but not found. Use keystone role-create to add it')
    if 'ResellerAdmin' not in role_names:
        raise SystemExit('[ERROR] Keystone should create "ResellerAdmin role '
                         'for swift service but not found. Use keystone '
                         'role-create to add it')

def check_ceilometer_role():
    """ceilometer needs 'admin' and 'ResellerAdmin' role."""
    ksclient = get_keystone_client()
    check_keystone_roles(ksclient)

    ceilometer_user_id = get_ceilometer_user_id(ksclient)
    service_tenant_id = get_service_tenant_id(ksclient)

    roles = ksclient.roles.roles_for_user(ceilometer_user_id,
                                          service_tenant_id)
    role_names = map(lambda role: role.name, roles)

    if '_member_' not in role_names:
        print ('[INFO] ceilometer should have _member_ role '
               'in service tenant but not found')
    if 'admin' not in role_names:
        raise SystemExit('[ERROR] ceilometer should have admin role '
                         'in service tenant but not found. Use keystone '
                         '"user-role-add --user ceilometer --tenant service '
                         '--role admin" to add it')
    if 'ResellerAdmin' not in role_names:
        raise SystemExit('[ERROR] ceilometer should have ResellerAdmin role '
                         'in service tenant but not found. Use keystone '
                         '"user-role-add --user ceilometer --tenant service '
                         '--role ResellerAdmin" to add it')

if __name__ == '__main__':
    check_ceilometer_role()
