# Kilo

| bp一句话描述 | bp解决的use case | bp链接 |
|:------|:---------|:-----|
| ceilometerclient支持显示能力列表 | 命令行下使用capabilities打印能力列表 | https://blueprints.launchpad.net/python-ceilometerclient/+spec/capability-cli |
| ceilometer支持event数据过期删除 | 当存储event数据时，使用ceilometer-expirer清理过期的event数据，防止数据库无限堆积 | https://blueprints.launchpad.net/ceilometer/+spec/event-database-ttl |
| ceilometerclient支持sample接口 | 命令行下使用sample-show打印具体的sample内容 | https://blueprints.launchpad.net/python-ceilometerclient/+spec/cli-samples-api |

| bug一句话描述 | bug的影响 | bug链接|
|:------|:---------|:-----|
| ceilometer hbase数据库场景下使用message signature生成唯一键值 | 在不对消息签名的场景下数据库出错 | https://bugs.launchpad.net/ceilometer/+bug/1445227 |
| ceilometer评估告警时没有捕获异常 | 一个告警出问题，该周期内剩余的告警都将无法评估 | https://bugs.launchpad.net/ceilometer/+bug/1408620 |
| ceilometer评估组合告警时对或操作处理不严谨 | 或操作组合告警时，其中一个告警但其他的为未知状态时，组合告警不会告警 | https://bugs.launchpad.net/ceilometer/+bug/1442613 |
| ceilometeclient没有对keystone session做超时处理 | 出现http卡死时，ceilometeclient所在线程停止工作 | https://bugs.launchpad.net/python-ceilometerclient/+bug/1436249 |
| ceilometerclient不支持多region访问 | 多region场景下，ceilometerclient无法正常工作 | https://bugs.launchpad.net/python-ceilometerclient/+bug/1439553 |
| ceilometer可以无限创建告警action | 普通用户可以利用此缺陷对系统进行攻击导致服务不可用|https://bugs.launchpad.net/ceilometer/+bug/1408248|
| ceilometer时间限制的告警在边界情况下工作异常 | 在特殊时间点，时间限制的告警容易出现无法正常评估的情况 | https://bugs.launchpad.net/ceilometer/+bug/1438674|
| novaclient总是记录操作时长 | 会造成用到novaclient的组件例如ceilometer-agent-compute出现内存泄露 | https://bugs.launchpad.net/python-novaclient/+bug/1433491 |
| ceilometer日志打印token | 安全相关，用户token泄露 | https://bugs.launchpad.net/ceilometer/+bug/1433004 |
| ceilometer没有使用配置文件中指定的数据库重连配置 | 进程行为和配置文件指定的不一致 | https://bugs.launchpad.net/ceilometer/+bug/1421485 |
| ceilometer SQL数据库场景下清理过期数据会破坏数据库 | 清理数据库时，resource相关的metadata表被破坏，导致后续根据metadata查询时失效 | https://bugs.launchpad.net/ceilometer/+bug/1419239 |
| ceilometer中调用http请求没有加上timeout | 容易在出现http请求卡死时，造成线程假死 | https://bugs.launchpad.net/ceilometer/+bug/1388778 |
