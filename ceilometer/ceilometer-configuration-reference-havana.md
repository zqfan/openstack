% OpenStack Ceilometer Havana API V2
%
%

| Copyright (c) 2014, Huawei Technologies Co., Ltd
|
| 	Licensed under the Apache License, Version 2.0 (the "License");
| 	you may not use this file except in compliance with the License.
| 	You may obtain a copy of the License at
|
| 	http://www.apache.org/licenses/LICENSE-2.0
|
| 	Unless required by applicable law or agreed to in writing, software
| 	distributed under the License is distributed on an "AS IS" BASIS,
| 	WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
| 	implied.
| 	See the License for the specific language governing permissions and
| 	limitations under the License.
|
| Author: ZhiQiang Fan <aji.zqfan@gmail.com>

This document summarizes configuration reference for Ceilometer Havana. You can read /etc/ceilometer/ceilometer.conf to get direct help information, and set non-default options by learning example from [openstack-manuals install guide](http://docs.openstack.org/trunk/install-guide/install/apt/content/ceilometer-install.html)

# 运维视角（Operator Perspective）
## 必选选项（Required）
以下选项若不设置，服务将无法正常运行，或者虽能运行但功能的正确性无法保障。

### ceilometer
你需要在ceilometer.conf中进行下列选项的设置

| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| connection | database | StrOpt | sqlite:////ceilometer/openstack/common/db/$sqlite_db | 数据库连接地址，例如connection = mongodb://ceilometer:CEILOMETER_DBPASS@controller:27017/ceilometer
| rabbit_host | DEFAULT | StrOpt | localhost | AMQP服务主机名或ip地址，推荐设置为控制节点ip或域名
| auth_host | keystone_authtoken | StrOpt | 127.0.0.1 | Keystone服务所在节点，推荐设置为控制节点ip或域名
| admin_user | keystone_authtoken | StrOpt | N/A | ceilometer用户名称，推荐设置为ceilometer（也可为admin但不推荐）
| admin_password | keystone_authtoken | StrOpt | N/A | ceilometer用户密码
| admin_tenant_name | keystone_authtoken | StrOpt | admin | ceilometer项目名称，推荐设置为service（也可为admin但不推荐）
| os_username | service_credentials | StrOpt | ceilometer | ceilometer用户名称，推荐设置为ceilometer
| os_password | service_credentials | StrOpt | admin | ceilometer用户密码
| os_tenant_name | service_credentials | StrOpt | service | ceilometer项目名称，推荐设置为service

### nova
你需要在nova.conf中进行下列选项的设置

| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| instance_usage_audit | DEFAULT | BoolOpt | false | Generate periodic compute.instance.exists notifications，是否允许nova进行审计，推荐保留默认设置，否则会对instance指标造成不必要的干扰
| instance_usage_audit_period | DEFAULT | StrOpt | month | time period to generate instance usages for.  Time period must be hour, day, month or year，推荐保留默认设置
| notify_on_state_change | DEFAULT | StrOpt | N/A | If set, send compute.instance.update notifications on instance state changes.  Valid values are None for no notifications, "vm_state" for notifications on VM state changes, or "vm_and_task_state" for notifications on VM and task state changes. 当虚拟机状态或者任务状态发生变化时发生通知，推荐保留默认设置，否则会对instance指标造成不必要的干扰
| notification_driver | DEFAULT | MultiStrOpt | N/A | Driver or drivers to handle sending notifications，消息驱动（这是一个可以多次设置的配置项），必须设置，推荐分别设置为nova.openstack.common.notifier.rpc_notifier和ceilometer.compute.nova_notifier

### glance
你需要在glance-api.conf中进行下列选项的设置

| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| notifier_strategy | DEFAULT | StrOpt | default | 通知策略,可以为logging, rabbit, qpid或者default, 默认为不发送通知.推荐设置为rabbit

### cinder
你需要在cinder.conf中进行下列选项的设置

| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| control_exchange | DEFAULT | StrOpt | openstack | AMQP exchange to connect to if using RabbitMQ or Qpid，消息队列频道，推荐设置为cinder
| notification_driver | DEFAULT | MultiStrOpt | N/A | Driver or drivers to handle sending notifications，消息驱动，推荐设置为cinder.openstack.common.notifier.rpc_notifier

### swift
swift与其他OpenStack核心项目不同，你需要在proxy-server.conf中设置

```
[filter:ceilometer]
use = egg:ceilometer#swift
[pipeline:main]
pipeline = healthcheck cache authtoken keystoneauth ceilometer proxy-server
```

即指定ceilometer过滤器加入api调用栈，这能够允许swift在操作时发送消息到ceilometer进行监控。

## 推荐选项（Recommended）
以下选项可以不设置，但性能及安全性将受到影响

| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| metering_secret | publisher_rpc | StrOpt | change this or be hacked | 对监测消息签名的密钥，默认值就是最好的提示，compute节点上此项配置必须和control节点上一致
| auth_protocol | keystone_authtoken | StrOpt | https | 身份验证协议，采用默认值即可。配置成https能提高安全性
| debug | DEFAULT | BoolOpt | False | 日志级别，采用默认值即可。打印DEBUG级别的日志，为true时会降低性能，仅在调测时打开。
| verbose | DEFAULT | BoolOpt | False | 日志详情，采用默认值即可。打印详细日志，为true时会降低性能，仅在调测时打开。

## 优化选项（Optimized）
以下选项若正确设置，能让你的工作更轻松愉快

| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| log_dir | DEFAULT | StrOpt | N/A | 日志目录，有的时候有的发布版的服务启动脚本没有添加这个选项导致日志都不见了，在配置文件中加上这个能保证总是有
| auth_uri | keystone_authtoken | StrOpt | N/A | 身份验证地址，推荐配置成形如https://controller:5000，能减少keystone报警

# 服务视角（Service Perspective）
## ceilometer
### ceilometer.alarm
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| rest_notifier_certificate_file | alarm | StrOpt | N/A | SSL Client certificate for REST notifier
| rest_notifier_certificate_key | alarm | StrOpt | N/A | SSL Client private key for REST notifier
| rest_notifier_ssl_verify | alarm | BoolOpt | true | Verify the SSL Server certificate when calling alarm action
| notifier_rpc_topic | alarm | StrOpt | alarm_notifier | the topic ceilometer uses for alarm notifier messages
| partition_rpc_topic | alarm | StrOpt | alarm_partition_coordination | the topic ceilometer uses for alarm partition coordination messages
| evaluation_interval | alarm | IntOpt | 60 | Period of evaluation cycle, should be >= than configured pipeline interval for collection of underlying metrics. 报警刷新周期，单位为秒，这个值最好比监控数据采集周期略小，否则易引起alarm状态非正常跳变。
| evaluation_service | alarm | StrOpt | ceilometer.alarm.service.SingletonAlarmService | Class to launch as alarm evaluation service 告警刷新服务驱动

### ceilometer.api
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| auth_strategy | DEFAULT | StrOpt | keystone | noauth or keystone. 身份验证策略，只能为noauth或者keystone。
| enable_v1_api | DEFAULT | BoolOpt | true | enable API V1 启用v1接口
| record_history | alarm | BoolOpt | true | Record alarm change events 记录报警变动信息
| port | api | IntOpt | 8777 | The port for the ceilometer API server api监听的端口
| host | api | StrOpt | 0.0.0.0 | The listen IP for the ceilometer API server api监听的地址

### ceilometer.collector
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| file_path | dispatcher_file | StrOpt | N/A | Name and the location of the file to record meters. 当数据持久化到文件时,文件的路径
| max_bytes | dispatcher_file | IntOpt | 0 | The max size of the file 持久化文件的大小上限
| backup_count | dispatcher_file | IntOpt | 0 | The max number of the files to keep 持久化文件备份数量
| udp_address | collector | StrOpt | 0.0.0.0 | address to bind the UDP socket to disabled if set to an empty string
| udp_port | collector | IntOpt | 4952 | port to bind the UDP socket to
| ack_on_event_error | collector | BoolOpt | true | Acknowledge message when event persistence fails
| store_events | collector | BoolOpt | false | Save event details
| dispatcher | collector | MultiStrOpt | database | dispatcher to process metering data 数据持久化策略,可以多次配置
| glance_control_exchange | DEFAULT | StrOpt | glance | Exchange name for Glance notifications 消息队列glance频道名称
| http_control_exchanges | DEFAULT | MultiStrOpt | [nova, glance, neutron, cinder] | Exchanges name to listen for notifications 消息队列监听的频道
| neutron_control_exchange | DEFAULT | StrOpt | neutron | Exchange name for Neutron notifications 消息队列neutron频道名称
| reseller_prefix | DEFAULT | StrOpt | AUTH_ | Swift reseller prefix. Must be on par with reseller_prefix in proxy-server.conf.
| cinder_control_exchange | DEFAULT | StrOpt | cinder | Exchange name for Cinder notifications 消息队列cinder频道名称

### ceilometer.compute
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| nova_control_exchange | DEFAULT | StrOpt | nova | exchagne name which receives nova notification 消息队列nova频道名称
| reserved_metadata_namespace | DEFAULT | ListOpt | metering. | list of metadata prefixes reserved for metering use
| reserved_metadata_length | DEFAULT | IntOpt | 256 | limit on length of reserved metadata values
| hypervisor_inspector | DEFAULT | StrOpt | libvirt | Inspector to use for inspecting the hypervisor layer
| libvirt_type | DEFAULT | StrOpt | kvm | Libvirt domain type (valid options are: kvm, lxc, qemu, uml, xen) 虚拟化管理器类型
| libvirt_uri | DEFAULT | StrOpt | N/A | Override the default libvirt URI (which is dependent on libvirt_type)

### 未明确的（unclassified）
#### ceilometer.pipeline
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| pipeline_cfg_file | DEFAULT | StrOpt | pipeline.yaml | Configuration file for pipeline definition

#### ceilometer.publisher
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| metering_topic | publisher_rpc | StrOpt | metring | the topic ceilometer uses for metering messages
| metering_secret | publisher_rpc | StrOpt | change this or be hacked | Secret value for signing metering messages 监控消息的签名密钥

#### ceilometer.sample
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| sample_source | DEFAULT | StrOpt | openstack | Source for samples emited on this instance 监控数据来源

#### ceilometer.service
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| os_username | service_credentials | StrOpt | ceilometer | Username to use for openstack service access 服务使用的用户名,必须有admin权限
| os_password | service_credentials | StrOpt | admin | Password to use for openstack service access 服务使用的密码
| os_tenant_id | service_credentials | StrOpt | N/A | Tenant ID to use for openstack service access 服务使用的项目id
| os_tenant_name | service_credentials | StrOpt | service | Tenant name to use for openstack service access 服务使用的项目名称
| os_cacert | service_credentials | StrOpt | N/A | Certificate chain for SSL validation
| os_auth_url | service_credentials | StrOpt | http://localhost:5000/v2.0 | Auth URL to use for openstack service access 服务身份验证地址
| os_region_name | service_credentials | StrOpt | N/A | Region name to use for openstack service endpoints
| os_endpoint_type | service_credentials | StrOpt | publicURL | Type of endpoint in Identity service catalog to use for communication with OpenStack services. 服务使用的地址类型

#### ceilometer.storage
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| database_connection | DEFAULT | StrOpt | N/A | DEPRECATED - Database connection string
| mysql_engine | DEFAULT | StrOpt | InnoDB | MySQL engine
| time_to_live | database | IntOpt | -1 | number of seconds that samples are kept in the database for (<= 0 means forever) 数据库中数据有效时间

## keystone
### keystoneclient.middleware.auth_token
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| auth_admin_prefix | keystone_authtoken | StrOpt | N/A | Prefix to prepend at the beginning of the path
| auth_host | keystone_authtoken | StrOpt | 127.0.0.1 | Host providing the admin Identity API endpoint
| auth_port | keystone_authtoken | IntOpt | 35357 | Port of the admin Identity API endpoint
| auth_protocol | keystone_authtoken | StrOpt | https | Protocol of the admin Identity API endpoint(http or https)
| auth_uri | keystone_authtoken | StrOpt | N/A | Complete public Identity API endpoint
| auth_version | keystone_authtoken | StrOpt | N/A | API version of the admin Identity API endpoint
| delay_auth_decision | keystone_authtoken | BoolOpt | false | Do not handle authorization requests within the middleware, but delegate the authorization decision to downstream WSGI components
| http_connect_timeout | keystone_authtoken | BoolOpt | N/A | Request timeout value for communicating with Identity API server.
| http_request_max_retries | keystone_authtoken | IntOpt | 3 | How many times are we trying to reconnect when communicating with Identity API Server.
| http_handler | keystone_authtoken | StrOpt | N/A | Allows to pass in the name of a fake http_handler callback function used instead of httplib.HTTPConnection or httplib.HTTPSConnection. Useful for unit testing where network is not available.
| admin_token | keystone_authtoken | StrOpt | N/A | Single shared secret with the Keystone configuration used for bootstrapping a Keystone installation, or otherwise bypassing the normal authentication process.
| admin_user | keystone_authtoken | StrOpt | N/A | Keystone account username
| admin_password | keystone_authtoken | StrOpt | N/A | Keystone account password
| admin_tenant_name | keystone_authtoken | StrOpt | admin | Keystone service account tenant name to validate user tokens
| cache | keystone_authtoken | StrOpt | N/A | Env key for the swift cache
| certfile | keystone_authtoken | StrOpt | N/A | Required if Keystone server requires client certificate
| keyfile | keystone_authtoken | StrOpt | N/A | Required if Keystone server requires client certificate
| cafile | keystone_authtoken | StrOpt | N/A | A PEM encoded Certificate Authority to use when verifying HTTPs connections. Defaults to system CAs.
| insecure | keystone_authtoken | BoolOpt | false | Verify HTTPS connections.
| signing_dir | keystone_authtoken | StrOpt | N/A | Directory used to cache files related to PKI tokens
| memcached_servers | keystone_authtoken | ListOpt | N/A | If defined, the memcache server(s) to use for caching
| token_cache_time | keystone_authtoken | IntOpt | 300 | In order to prevent excessive requests and validations, the middleware uses an in-memory cache for the tokens the Keystone API returns. This is only valid if memcache_servers is defined. Set to -1 to disable caching completely.
| revocation_cache_time | keystone_authtoken | IntOpt | 1 | Value only used for unit testing
| memcache_security_strategy | keystone_authtoken | StrOpt | N/A | (optional) if defined, indicate whether token data should be authenticated or authenticated and encrypted. Acceptable values are MAC or ENCRYPT.  If MAC, token data is authenticated (with HMAC) in the cache. If ENCRYPT, token data is encrypted and authenticated in the cache. If the value is not one of these options or empty, auth_token will raise an exception on initialization.
| memcache_secret_key | keystone_authtoken | StrOpt | N/A | (optional, mandatory if memcache_security_strategy is defined) this string is used for key derivation.

# oslo
| Option | Section | Type | Default | Description |
|:-------|:--------|:-----|:--------|:------------|
| sqlite_db | DEFAULT | StrOpt | ceilometer.sqlite | the filename to use with sqlite
| sqlite_synchronous | DEFAULT | BoolOpt | true | If true, use synchronous mode for sqlite
| debug | DEFAULT | BoolOpt | False | Print debugging output (set logging level to DEBUG instead of default WARNING level).
| verbose | DEFAULT | BoolOpt | False | Print more verbose output (set logging level to INFO instead of default WARNING level).
| backdoor_port | DEFAULT | StrOpt | N/A | Enable eventlet backdoor.  Acceptable values are 0, <port>, and <start>:<end>, where 0 results in listening on a random tcp port number; <port> results in listening on the specified port number (and not enabling backdoor if that port is in use); and <start>:<end> results in listening on the smallest unused port number within the specified range of port numbers.  The chosen port is displayed in the service's log file.
| disable_process_locking | DEFAULT | BoolOpt | false | Whether to disable inter-process locks
| lock_path | DEFAULT | StrOpt | N/A | Directory to use for lock files.
| use_stderr | DEFAULT | BoolOpt | true | Log output to standard error
| logging_context_format_string | DEFAULT | StrOpt | %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(request_id)s %(user)s %(tenant)s] %(instance)s%(message)s | format string to use for log messages with context
| logging_default_format_string | DEFAULT | StrOpt | %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s | format string to use for log messages without context
| logging_debug_format_suffix | DEFAULT | StrOpt | %(funcName)s %(pathname)s:%(lineno)d | data to append to log format when level is DEBUG
| logging_exception_prefix | DEFAULT | StrOpt | %(asctime)s.%(msecs)03d %(process)d TRACE %(name)s %(instance)s | prefix each line of exception output with this format
| default_log_levels | DEFAULT | ListOpt | amqplib=WARN,sqlalchemy=WARN,boto=WARN,suds=INFO,keystone=INFO,eventlet.wsgi.server=WARN | list of logger=LEVEL pairs
| publish_errors | DEFAULT | BoolOpt | false | publish error events
| fatal_deprecations | DEFAULT | BoolOpt | false | make deprecations fatal
| instance_format | DEFAULT | StrOpt | "[instance: %(uuid)s] " | If an instance is passed with the log message, format it like this
| instance_uuid_format | DEFAULT | StrOpt | "[instance: %(uuid)s] " | If an instance UUID is passed with the log message, format it like this
| log_config | DEFAULT | StrOpt | N/A | If this option is specified, the logging configuration file specified is used and overrides any other logging options specified. Please see the Python logging module documentation for details on logging configuration files.
| log_format | DEFAULT | StrOpt | N/A | DEPRECATED. A logging.Formatter log message format string which may use any of the available logging.LogRecord attributes. This option is deprecated.  Please use logging_context_format_string and logging_default_format_string instead.
| log_date_format | DEFAULT | StrOpt | %Y-%m-%d %H:%M:%S | Format string for %%(asctime)s in log records. Default: %(default)s
| log_file | DEFAULT | StrOpt | N/A | (Optional) Name of log file to output to. If no default is set, logging will go to stdout.
| log_dir | DEFAULT | StrOpt | N/A | (Optional) The base directory used for relative --log-file paths
| use_syslog | DEFAULT | BoolOpt | false | Use syslog for logging.
| syslog_log_facility | DEFAULT | StrOpt | LOG_USER | syslog facility to receive log lines
| notification_driver | DEFAULT | StrOpt | N/A | Driver or drivers to handle sending notifications
| default_notification_level | DEFAULT | StrOpt | INFO | Default notification level for outgoing notifications
| default_publisher_id | DEFAULT | StrOpt | N/A | Default publisher_id for outgoing notifications
| notification_topics | DEFAULT | StrOpt | notifications | AMQP topic used for openstack notifications
| policy_file | DEFAULT | StrOpt | policy.json | JSON file containing policy
| policy_default_rule | DEFAULT | StrOpt | default | Rule enforced when requested rule is not found
| rpc_backend | DEFAULT | StrOpt | ceilometer.openstack.common.rpc.impl_kombu | The messaging module to use, defaults to kombu.
| rpc_thread_pool_size| DEFAULT | IntOpt | 64 | Size of RPC thread pool
| rpc_conn_pool_size | DEFAULT | IntOpt | 30 | Size of RPC connection pool
| rpc_response_timeout | DEFAULT | IntOpt | 60 | Seconds to wait for a response from call or multicall
| rpc_cast_timeout | DEFAULT | IntOpt | 30 | Seconds to wait before a cast expires (TTL). Only supported by impl_zmq
| allowed_rpc_exception_modules | DEFAULT | ListOpt | ceilometer.openstack.common.exception,nova.exception,cinder.exception,exceptions | Modules of exceptions that are permitted to be recreatedupon receiving exception data from an rpc call.
| fake_rabbit | DEFAULT | BoolOpt | false | If passed, use a fake RabbitMQ provider
| control_exchange | DEFAULT | StrOpt | openstack | AMQP exchange to connect to if using RabbitMQ or Qpid
| amqp_durable_queues | DEFAULT | BoolOpt | false | Use durable queues in amqp.
| amqp_auto_delete | DEFAULT | BoolOpt | false | Auto-delete queues in amqp.
| kombu_ssl_version | DEFAULt | StrOpt | N/A | SSL version to use (valid only if SSL enabled). valid values are TLSv1, SSLv23 and SSLv3. SSLv2 may be available on some distributions
| kombu_ssl_keyfile | DEFAULT | StrOpt | N/A | SSL key file (valid only if SSL enabled)
| kombu_ssl_certfile | DEFAULT | StrOpt | N/A | SSL cert file (valid only if SSL enabled)
| kombu_ssl_ca_certs | DEFAULT | StrOpt | N/A | SSL certification authority file (valid only if SSL enabled)
| rabbit_host | DEFAULT | StrOpt | localhost | The RabbitMQ broker address where a single node is used
| rabbit_port | DEFAULT | IntOpt | 5672 | The RabbitMQ broker port where a single node is used
| rabbit_hosts | DEFAULT | ListOpt | $rabbit_host:$rabbit_port | RabbitMQ HA cluster host:port pairs
| rabbit_use_ssl | DEFAULT | BoolOpt | false | connect over SSL for RabbitMQ
| rabbit_userid | DEFAULT | BoolOpt | guest | the RabbitMQ userid
| rabbit_password | DEFAULT | StrOpt | guest | the RabbitMQ password
| rabbit_virtual_host | DEFAULT | StrOpt | / | the RabbitMQ virtual host
| rabbit_retry_interval | DEFAULT | IntOpt | 1 | how frequently to retry connecting with RabbitMQ
| rabbit_retry_backoff | DEFAULT | IntOpt | 2 | how long to backoff for between retries when connecting to RabbitMQ
| rabbit_max_retries | DEFAULT | IntOpt | 0 | maximum retries with trying to connect to RabbitMQ (the default of 0 implies an infinite retry count)
| rabbit_ha_queues | DEFAULT | BoolOpt | false | use H/A queues in RabbitMQ (x-ha-policy: all).You need to wipe RabbitMQ database when changing this option.
| qpid_hostname | DEFAULT | StrOpt | localhost | Qpid broker hostname
| qpid_port| DEFAULT | IntOpt | 5672 | Qpid broker port
| qpid_hosts | DEFAULT | ListOpt | $qpid_hostname:$qpid_port | Qpid HA cluster host:port pairs
| qpid_username| DEFAULT | StrOpt | N/A | Username for qpid connection
| qpid_password | DEFAULT | StrOpt | N/A | Password for qpid connection
| qpid_sasl_mechanisms | DEFAULT | StrOpt | N/A | Space separated list of SASL mechanisms to use for auth
| qpid_heartbeat | DEFAULT | IntOpt | 60 | Seconds between connection keepalive heartbeats
| qpid_protocol | DEFAULT | StrOpt | tcp | Transport to use, either 'tcp' or 'ssl'
| qpid_tcp_nodelay| DEFAULT | BoolOpt | true | Disable Nagle algorithm
| qpid_topology_version | DEFAULT | IntOpt | 1 | The qpid topology version to use.  Version 1 is what was originally used by impl_qpid.  Version 2 includes some backwards-incompatible changes that allow broker federation to work.  Users should update to version 2 when they are able to take everything down, as it requires a clean break.
| rpc_zmq_bind_address | DEFAULT | StrOpt | * | ZeroMQ bind address. Should be a wildcard, an ethernet interface, or IP. The "host" option should point or resolve to this address.
| rpc_zmq_matchmaker | DEFAULT | StrOpt |  ceilometer.openstack.common.rpc.matchmaker.MatchMakerLocalhost | MatchMaker driver
| rpc_zmq_port | DEFAULT | IntOpt | 9501 | ZeroMQ receiver listening port
| rpc_zmq_contexts | DEFAULt | IntOpt | 1 | Number of ZeroMQ contexts, defaults to 1
| rpc_zmq_topic_backlog | DEFAULT | IntOpt | N/A | Maximum number of ingress messages to locally buffer per topic. Default is unlimited.
| rpc_zmq_ipc_dir | DEFAULT | StrOpt | /var/run/openstack | Directory for holding IPC sockets
| rpc_zmq_host | DEFAULT | StrOpt | ceilometer | Name of this node. Must be a valid hostname, FQDN, or IP address. Must match "host" option, if running Nova.
| matchmaker_heartbeat_freq | DEFAULT | IntOpt | 300 | Heartbeat frequency
| matchmaker_heartbeat_ttl | DEFAULT | IntOpt | 600 | Heartbeat time-to-live
| ca_file | ssl | StrOpt | N/A | CA certificate file to use to verify connecting clients
| cert_file | ssl | StrOpt | N/A | Certificate file to use when starting the server securely
| key_file | ssl | StrOpt | N/A | Private key file to use when starting the server securely
| backend | database | StrOpt | sqlalchemy | The backend to use for db
| use_tpool | database | BoolOpt | false | Enable the experimental use of thread pooling for all DB API calls
| connection | database | StrOpt | sqlite:////ceilometer/openstack/common/db/$sqlite_db | The SQLAlchemy connection string used to connect to the database
| slave_connection | database StrOpt | N/A | The SQLAlchemy connection string used to connect to the slave database
| idle_timeout | database | IntOpt | 3600 | timeout before idle sql connections are reaped
| min_pool_size | database | IntOpt | 1 | Minimum number of SQL connections to keep open in a pool
| max_pool_size | database | IntOpt | N/A | Maximum number of SQL connections to keep open in a pool
| max_retries | database | IntOpt | 10 | maximum db connection retries during startup. (setting -1 implies an infinite retry count)
| retry_interval | database | IntOpt | 10 | interval between retries of opening a sql connection
| max_overflow | database | IntOpt | N/A | If set, use this value for max_overflow with sqlalchemy
| connection_debug | database | IntOpt | 0 | Verbosity of SQL debugging information. 0=None, 100=Everything
| connection_trace | database | BoolOpt | false | Add python stack traces to SQL as comment strings
| pool_timeout | database | IntOpt | N/A | If set, use this value for pool_timeout with sqlalchemy
| topics | rpc_notifier2 | ListOpt | notifications | AMQP topic(s) used for openstack notifications
| ringfile | matchmaker_ring | StrOpt | /etc/oslo/matchmaker_ring.json | Matchmaker ring file (JSON)
| host | matchmaker_redis | StrOpt | 127.0.0.1 | Host to locate redis
| port | matchmaker_redis | IntOpt | 6379 | Use this port to connect to redis host.
| password | matchmaker_redis | StrOpt | N/A | Password for Redis server.
