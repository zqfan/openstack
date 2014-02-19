% OpenStack Ceilometer Havana API V2
%
%

| Copyright (c) 2014, Huawei Technologies Co., Ltd
|
| Licensed under the Apache License, Version 2.0 (the "License");
| you may not use this file except in compliance with the License.
| You may obtain a copy of the License at
|
| http://www.apache.org/licenses/LICENSE-2.0
|
| Unless required by applicable law or agreed to in writing, software
| distributed under the License is distributed on an "AS IS" BASIS,
| WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
| implied.
| See the License for the specific language governing permissions and
| limitations under the License.
|
| Author: ZhiQiang Fan <aji.zqfan@gmail.com>

# 前言 {#preface}
本文档描述OpenStack Ceilometer项目Havana版本ReST API V2，主要依据

* http://api.openstack.org/api-ref-telemetry.html
* http://docs.openstack.org/developer/ceilometer/

在SLES 11 SP3上对Ceilometer 2013.2.2进行验证，使用的数据库为mongodb。

文档修改历史

------------------------------------------------------------------------------------------
修改时间   修改概述                                                               修改者
---------- ---------------------------------------------------------------------  ---------
2014-02-19 1、文档json示例按照模板编写；\                                         f00253402
           2、修正若干错误

2014-02-15 1、修正了描述错误的接口，获取指定meter的statistics，由POST改为了GET；\ f00253402
           2、文档整体结构按照模板填写；\
           3、将模型中未定义的字段由-改为了N/A；\
           4、进一步改善正确性和可使用性

2014-02-11 初稿	                                                                  f00253402
------------------------------------------------------------------------------------------

# 概述

## 词汇表

| 名称 | 含义 |
|:----|:----|
| meter | 度量，指标
| sample | 采样，数据点
| statistic | 统计
| alarm | 告警
| Resource | 资源

# 对象模型
Ceilometer Havana API V2管理如下对象

## Resource

* Resource属性表

| 属性 | 类型 | CRUD | 默认值 | 约束 | 备注 |
|:-----|:-----|:-----|:-------|:-----|:-----|
| resource_id | string | r | N/A | N/A | 资源id，与其他服务中对应资源的id一致
| project_id | string | r | N/A | N/A | 项目id，即用户所在租户id
| user_id | string | r | N/A | N/A | 用户id
| source | string | r | N/A | N/A | 来源，其他组件发出的rpc可能将其设置为openstack
| meter | string | r | N/A | N/A | 此资源上的meter列表，最新havana分支中以冗余为由已被移除
| first_sample_timestamp | date string | r | N/A | N/A | 数据采集最初UTC时间
| last_sample_timestamp | date string | r | N/A | N/A | 数据采集最近UTC时间
| metadata | string | r | N/A | N/A | 资源元数据，格式化的json对象

## Meter
Meter是资源可监测的类型，注：数据库中的meter表实际存储的是sample

* meter属性表

| 属性 | 类型 | CRUD | 默认值 | 约束 | 备注 |
|:-----|:-----|:-----|:-------|:-----|:-----|
| name | string | r | N/A | N/A | 名称，唯一
| type | string | r | N/A | 见type取值表 | 类型，只能为gauge，cumulative，delta之一
| unit | string | r | N/A | N/A | 单位
| resource_id | string | r | N/A | N/A | 资源id
| project_id | string | r | N/A | N/A | 项目id
| source | string | r | N/A | N/A | 来源
| user_id | string | r | N/A | N/A | 用户id

* type取值表

| 值 | 备注 |
|:---|:-----|
| gauge | 离散值，如虚拟机个数
| cumulative | 连续值，如网卡流量
| delta | 增量值，如进度条

## Sample
Sample是一个数据点，可以理解为在某一时间点上对某个Meter的采样，对应数据库中的meter表。

* Sample属性表

| 属性 | 类型 | CRUD | 默认值 | 约束 | 备注 |
|:-----|:-----|:-----|:-------|:-----|:-----|
| source | string | cr | N/A | N/A | 名称
| counter_name | string | cr | N/A | N/A | meter名称
| counter_type | string | cr | N/A | N/A | meter类型
| counter_unit | string | cr | N/A | N/A | meter单位
| counter_volume | string | cr | N/A | N/A | 值
| user_id | string | cr | N/A | N/A | 用户id
| project_id | string | cr | N/A | N/A | 项目id
| resource_id | string | cr | N/A | N/A | 资源id
| timestamp | date string | r | N/A | N/A | 时间戳
| resource_metadata | string | cr | N/A | N/A | 资源元数据（和resource冗余吗？）
| message_id | string | r | N/A | N/A | 消息id
| message_signature | string | r | N/A | N/A | 消息数据的hash值

## Statistics
Statistic是Sample的统计。

* Statistics属性表

| 属性 | 类型 | CRUD | 默认值 | 约束 | 备注 |
|:-----|:-----|:-----|:-------|:-----|:-----|
| unit | string | r | N/A | N/A | 单位
| min | string | r | N/A | N/A | 最小值
| max | string | r | N/A | N/A | 最大值
| avg | string | r | N/A | N/A | 平均值
| sum | string | r | N/A | N/A | 总和
| count | string | r | N/A | N/A | 数量
| period | string | r | N/A | N/A | 周期，单位秒
| period_start | date string | r | N/A | N/A | 周期起始时间
| period_end | date string | r | N/A | N/A | 周期结束时间
| duration | string | r | N/A | N/A | 持续时间
| duration_start | date string | r | N/A | N/A | 持续时间起始时间
| duration_end | date string | r | N/A | N/A | 持续时间结束时
| groupby | string | r | N/A | N/A | sample分组

## Alarm
alarm对应数据库alarm表

* Alarm属性表

| 属性 | 类型 | CRUD | 默认值 | 约束 | 备注 |
|:-----|:-----|:-----|:-------|:-----|:-----|
| alarm_id | string | r | N/A | N/A | uuid
| type | string | crw | N/A | N/A | 类型，取值为threshold或combination
| name | string | crw | N/A | N/A | 名称，项目内唯一
| description | string | crw | 有 | N/A | 描述，默认值根据类型而不同
| enabled | string | crw | N/A | N/A | 是否可用
| state | string | crw | N/A | 见state取值表 | 状态，取值为ok/alarm/insufficient data
| rule | string | crw | N/A | N/A | 条件，满足条件即触发alarm
| user_id | string | crw | N/A | N/A | 用户id
| project_id | string | crw | N/A | N/A | 项目id
| evaluation_periods | string | crw | N/A | N/A | 时间窗口数量
| period | string | crw | N/A | N/A | 时间窗口，单位秒
| timestamp | date string | r | N/A | N/A | 最后一次更新的时间戳
| state_timestamp | date string | r | N/A | N/A | 最后一次状态更新的时间戳
| ok_actions | string | crw | N/A | N/A | alarm状态跃迁为ok时执行的动作
| alarm_actions | string | crw | N/A | N/A | alarm状态跃迁为alarm时执行的动作
| insufficient_data_actions	| string | crw | N/A | N/A | alarm状态跃迁为insufficient data时执行的动作
| repeat_actions | string | crw | N/A | N/A | 是否重复执行动作

* state取值表

| 值 | 备注 |
|:---|:-----|
| ok | 正常
| alarm | 警报
| insufficient data | 数据不正确

## AlarmChange
AlarmChange对应数据库alarm_history表。

* AlarmChange属性表

| 属性 | 类型 | CRUD | 默认值 | 约束 | 备注 |
|:-----|:-----|:-----|:-------|:-----|:-----|
| event_id | string | r | N/A | N/A | 事件的uuid
| alarm_id | string | r | N/A | N/A | alarm id
| type | string | r | N/A | N/A | alarm变动的类型
| detail | string | r | N/A | N/A | alarm变动的细节
| user_id | string | r | N/A | N/A | 用户id，alarm初始用户
| project_id | string | r | N/A | N/A | 项目id，alarm初始项目
| on_behalf_of | string | r | N/A | N/A | 项目id，alarm变动后归属的项目
| timestamp |  datetime | r | N/A | N/A | 时间戳

# API通用信息
## 获取token
Ceilometer API v2使用Keystone Identity Service作为默认的鉴权服务，用户向Ceilometer API发送请求，请求的HTTP Head中必须包括一个X-Auth-Token参数，X-Auth-Token的值必须是一个经过Keystone授权分配的token，通过Keystone分配token的方法，请查阅Keystone的接口文档。

HTTP 消息样例：

| Element | Content |
|:--------|:--------|
| HTTP HEAD	| X-Auth-Token：9c81513600564b31b32d5918963778b3 Content-type：application/json
| HTTP BODY | {...}

## 多租户支持
Ceilometer中大部分对象都具有租户属性，如果是资源相关的对象，租户属性从资源中取得，如果是Alarm对象，租户属性在创建、修改Alarm时由http头部信息中的X-Project-Id获得，或者在消息体中指定。

# API操作
## 资源（Resource）
### 查询资源（List Resources）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/resources?q.op={operator}&q.value={value}&q.field={field} | 获取Resource列表

* request filter参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| q.op | string | 见op表 | No | 操作符
| q.value | string | N/A | No | 值
| q.field | string | 见filed表 | No | 查询关键字

op表

| 可选值 | 约束 | 备注 |
|:-------|:-----|:-----|
| eq | field!=timpestamp | 等于
| lt | field=timestamp | 小于
| le | field=timestamp | 小于等于
| ge | field=timestamp | 大于等于
| gt | field=timestamp | 大于

field表

| 可选值 | 备注 |
|:-------|:-----|
| resource | 资源id
| project | 项目id
| user | 用户id
| source | 来源名称
| timestamp | 时间戳，未定义但有效
| start_timestamp | 起始时间戳，合法但无效
| end_timpestamp | 结束时间戳，合法但无效
| start_timestamp_op | 起始时间戳操作符，合法但无效
| end_timpestamp_op | 结束时间戳操作符，合法但无效
| metadata | 元数据
| pagination | 未实现

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| |
+=+
| GET /v2/resources |
+-+
| N/A |
+-+

* JSON响应样例

+-+
| STATUS CODE 200 |
+-+
| ```json
|  [ |
|      { |
|          "first_sample_timestamp": "2014-01-09T11:11:22.946000", |
|          "last_sample_timestamp": "2014-01-09T11:11:22.946000", |
|          "links": [ |
|              { |
|                  "href": "http://controller:8777/v2/resources/0f2ab214-103a-4111-919b-c0cdd03db629", |
|                  "rel": "self" |
|              }, |
|              { |
|                  "href": "http://controller:8777/v2/meters/network?q.field=resource_id&q.value=0f2ab214-103a-4111-919b-c0cdd03db629", |
|                  "rel": "network" |
|              }, |
|              { |
|                  "href": "http://controller:8777/v2/meters/network.create?q.field=resource_id&q.value=0f2ab214-103a-4111-919b-c0cdd03db629", |
|                  "rel": "network.create" |
|              } |
|          ], |
|          "metadata": { |
|              "admin_state_up": "True", |
|              "event_type": "network.create.end", |
|              "host": "network.aio", |
|              "id": "0f2ab214-103a-4111-919b-c0cdd03db629", |
|              "name": "int-net", |
|              "provider:network_type": "local", |
|              "provider:physical_network": "None", |
|              "provider:segmentation_id": "None", |
|              "shared": "False", |
|              "status": "ACTIVE", |
|              "tenant_id": "313a8bc21b994e60b93d6fff7c1e0c1b" |
|          }, |
|          "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b", |
|          "resource_id": "0f2ab214-103a-4111-919b-c0cdd03db629", |
|          "user_id": "30aee73695744a6096e35fdab25b6766" |
|      } |
|  ] |
| ``` |
+-+

* 过滤条件JSON请求样例，metaquery


+-+
| GET /v2/resources?q.op=eq&q.value=network.nonexistenthostname&q.field=metadata.host |
+-+
| N/A |
+-+

* 过滤条件JSON响应样例，metaquery

由于metadata键值为host，值为nonexistentHostName的resource并不存在，输出为空

+-+
| STATUS CODE 200 |
+-+
| ```json |
| [] |
| ``` |
+-+

### 查询资源详情（Show Resource）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/resources/{resource_id} | 获取指定资源信息

* request filter参数

无

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/resources/0f2ab214-103a-4111-919b-c0cdd03db629 |
+-+
| N/A |
+-+

* JSON响应样例

+-+
| STATUS CODE 200 |
+-+
| ```json |
| { |
|    "first_sample_timestamp": "2014-01-09T11:11:22.946000", |
|     "last_sample_timestamp": "2014-01-09T11:11:22.946000", |
|     "links": [ |
|         { |
|             "href": "http://controller:8777/v2/resources/0f2ab214-103a-4111-919b-c0cdd03db629", |
|             "rel": "self" |
|         }, |
|         { |
|             "href": "http://controller:8777/v2/meters/network?q.field=resource_id&q.value=0f2ab214-103a-4111-919b-c0cdd03db629", |
|             "rel": "network" |
|         }, |
|         { |
|             "href": "http://controller:8777/v2/meters/network.create?q.field=resource_id&q.value=0f2ab214-103a-4111-919b-c0cdd03db629", |
|             "rel": "network.create" |
|         } |
|     ], |
|     "metadata": { |
|         "admin_state_up": "True", |
|         "event_type": "network.create.end", |
|         "host": "network.aio", |
|         "id": "0f2ab214-103a-4111-919b-c0cdd03db629", |
|         "name": "int-net", |
|         "provider:network_type": "local", |
|         "provider:physical_network": "None", |
|         "provider:segmentation_id": "None", |
|         "shared": "False", |
|         "status": "ACTIVE", |
|         "tenant_id": "313a8bc21b994e60b93d6fff7c1e0c1b" |
|     }, |
|     "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b", |
|     "resource_id": "0f2ab214-103a-4111-919b-c0cdd03db629", |
|     "user_id": "30aee73695744a6096e35fdab25b6766" |
| } |
| ``` |
+-+

## 度量（Meter）
### 查询度量（List Meters）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/meters?q.op=eq&q.value={value}&q.field={field} | 获取Meter列表

* request filter参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| q.op | string | 只能为eq | No | 操作符
| q.value | string | N/A | No | 值
| q.field | string | 见filed表 | No | 查询关键字

field表

| 可选值 | 备注 |
|:-------|:-----|
| resource | 资源id
| project | 项目id
| user | 用户id
| source | 来源名称
| metadata | 元数据，无效
| pagination | 未实现

* request body参数

无

* response body参数
待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/meters
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "meter_id": "MTEzNDcwMmQtNDcxZS00MjYwLWEzNWMtMTk3Mzg5OTI2MzZiK2ltYWdl\n",
|         "name": "image",
|         "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b",
|         "resource_id": "1134702d-471e-4260-a35c-19738992636b",
|         "source": "openstack",
|         "type": "gauge",
|         "unit": "image",
|         "user_id": null
|     }
| ]
| ```
+-+

* 过滤条件JSON请求样例，source

+-+
| GET  /v2/meters?q.op=eq&q.value=orcs&q.field=source
+-+
| N/A
+-+

* 过滤条件JSON响应样例，source

由于来源自orcs的meter并不存在，输出为空

+-+
| STATUS CODE 200
+-+
| ```json
| []
| ```
+-+

## 数据点（Sample）
### 查询数据点（List Samples）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/meters/{meter_name}?limit={value}&q.op=eq&q.value={value}&q.field={field} | 获取指定Meter下所有的数据点

* request filter参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| q.op | string | 只能为eq | No | 操作符
| q.value | string | N/A | No | 值
| q.field | string | 见filed表 | No | 查询关键字
| limit | int | N/A | No | 返回结果数

field表

| 可选值 | 约束 | 备注 |
|:-------|:-----|:-----|
| resource | N/A | 资源id
| project | N/A | 项目id
| user | N/A | 用户id
| source | N/A | 来源名称
| start | N/A | 起始时间戳
| end | N/A | 结束时间戳
| start_timestamp_op | 见tsop表 | 起始时间戳操作符
| end_timpestamp_op | 见tsop表 | 结束时间戳操作符
| metadata | N/A | 元数据
| meter | N/A | 度量

tsop表

| 可选值 | 备注 |
|:-------|:-----|
| eq | 等于
| lt | 小于
| le | 小于等于
| ge | 大于等于
| gt | 大于

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/meters/router
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "counter_name": "router",
|         "counter_type": "gauge",
|         "counter_unit": "router",
|         "counter_volume": 1.0,
|         "message_id": "dbfb95b6-791e-11e3-866f-548998f6e71d",
|         "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b",
|         "resource_id": "a67d5d0d-1ad1-4402-99be-192b946dd5cc",
|         "resource_metadata": {
|             "admin_state_up": "True",
|             "event_type": "router.create.end",
|             "external_gateway_info": "None",
|             "host": "network.aio",
|             "id": "a67d5d0d-1ad1-4402-99be-192b946dd5cc",
|             "name": "admin-router",
|             "status": "ACTIVE",
|             "tenant_id": "313a8bc21b994e60b93d6fff7c1e0c1b"
|         },
|         "source": "openstack",
|         "timestamp": "2014-01-09T11:11:59.772000",
|         "user_id": "30aee73695744a6096e35fdab25b6766"
|     }
| ]
| ```
+-+

* 过滤条件JSON请求样例，limit

+-+
| GET /v2/meters/router?limit=1
+-+
| N/A
+-+

* 过滤条件JSON响应样例，limit

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "counter_name": "instance",
|         "counter_type": "gauge",
|         "counter_unit": "instance",
|         "counter_volume": 1.0,
|         "message_id": "c4841b8c-91b1-11e3-b763-548998f6e71d",
|         "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b",
|         "resource_id": "7fd9bc47-dfbf-418f-9355-4650f32a0456",
|         "resource_metadata": {
|             "OS-EXT-AZ:availability_zone": "nova",
|             "disk_gb": "1",
|             "display_name": "test",
|             "ephemeral_gb": "0",
|             "flavor.disk": "1",
|             "flavor.ephemeral": "0",
|             "flavor.id": "1",
|             "flavor.name": "m1.tiny",
|             "flavor.ram": "512",
|             "flavor.vcpus": "1",
|             "host": "53ae8c96454e4c700e3d3fa28beb66d17157b7ea501d47a08cb8540c",
|             "image.id": "d338a0f7-ef81-43bb-b098-7de14fd1449d",
|             "image.name": "cirros0.3.1",
|             "image_ref": "d338a0f7-ef81-43bb-b098-7de14fd1449d",
|             "image_ref_url": "http://controller:8774/aebb7f33b7fc4cf486d3a2cdacac8ac1/images/d338a0f7-ef81-43bb-b098-7de14fd1449d",
|             "instance_type": "1",
|             "kernel_id": "None",
|             "memory_mb": "512",
|             "name": "instance-00000016",
|             "ramdisk_id": "None",
|             "root_gb": "1",
|             "vcpus": "1"
|         },
|         "source": "openstack",
|         "timestamp": "2014-02-09T17:44:04",
|         "user_id": "30aee73695744a6096e35fdab25b6766"
|     }
| ]
| ```
+-+

### 创建数据点（Create Sample）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| POST | /v2/meters/{meter_name} | 为指定Meter创建数据点

* request filter参数

无

* request body参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| N/A | list | N/A | Yes | Sample数据

Sample结构

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| counter_name | string | N/A | YES | 度量名称
| counter_type | string | YES | YES | 度量类型
| counter_unit | string | N/A | YES | 度量单位
| counter_volume | float | N/A | YES | 度量值
| resource_id | string | N/A | YES | 资源id
| project_id | string | admin可指定 | NO | 项目id
| user_id | string | admin可指定 | NO | 用户id
| resource_metadata	string | json object | NO | 资源元数据
| timestamp | date string | 必须为时间格式 | NO | 时间戳
| message_signature | string | N/A | NO | 消息签名，可以设置但没有效果

couter_type可选值

| 可选值 | 备注 |
|:-------|:-----|
| gauge | 离散值，如虚拟机个数
| cumulative | 连续值，如网卡流量
| delta | 增量值，如进度条

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| POST /v2/meters/router
+-+
| ```json
| [
|     {
|         "counter_name": "router",
|         "counter_type": "gauge",
|         "counter_unit": "router",
|         "counter_volume": "1",
|         "resource_id": "x"
|     }
| ]
| ```
+-+

* JSON响应样例

HTTP POST成功一般会返回CODE 201 CREATED，此处ceilometer返回200也是可以的

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "counter_name": "router",
|         "counter_type": "gauge",
|         "counter_unit": "router",
|         "counter_volume": 1.0,
|         "message_id": "90919fdc-927b-11e3-9310-548998f6e71d",
|         "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b",
|         "resource_id": "x",
|         "resource_metadata": {},
|         "source": "313a8bc21b994e60b93d6fff7c1e0c1b:openstack",
|         "timestamp": "2014-02-10T17:48:35.533491",
|         "user_id": "30aee73695744a6096e35fdab25b6766"
|     }
| ]
| ```
+-+

## 统计（Statistics）
### 查询统计（Show Statistics）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/meters/{meter_name}/statistics?period={value}& q.op=eq&q.value={value}&q.field={field}&groupby={value} | 获取指定meter的统计信息

* request filter参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| q.op | string | 只能为eq | No | 操作符
| q.value | string | N/A | No | 值
| q.field | string | 见filed取值表 | No | 查询关键字
| period | int | 非负数 | No | 间隔
| groupby | string | 见groupby取值表 | No | 分组

field取值表

| 可选值 | 备注 |
|:-------|:-----|
| resource | 资源id
| project | 项目id
| user | 用户id
| source | 来源名称
| start | 起始时间戳
| end | 结束时间戳
| start_timestamp_op | 起始时间戳操作符，见tsop取值表
| end_timpestamp_op | 结束时间戳操作符，见tsop取值表
| metadata | 元数据
| meter | 无效

tsop取值表

| 可选值 | 备注 |
|:-------|:-----|
| eq | 等于
| lt | 小于
| le | 小于等于
| ge | 大于等于
| gt | 大于

groupby取值表

| 可选值 | 备注 |
|:-------|:-----|
| resource_id | 资源id
| project_id | 项目id
| user_id | 用户id
| source | 来源

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/meters/router/statistics
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "avg": 1.0,
|         "count": 1,
|         "duration": 0.0,
|         "duration_end": "2014-01-09T11:11:59.772000",
|         "duration_start": "2014-01-09T11:11:59.772000",
|         "groupby": null,
|         "max": 1.0,
|         "min": 1.0,
|         "period": 0,
|         "period_end": "2014-01-09T11:11:59.772000",
|         "period_start": "2014-01-09T11:11:59.772000",
|         "sum": 1.0,
|         "unit": "router"
|     }
| ]
| ```
+-+

* 过滤条件JSON请求样例，period

+-+
| GET /v2/meters/router/statistics?period=10
+-+
| N/A
+-+

* 过滤条件JSON响应样例，period

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "avg": 1.0,
|         "count": 1,
|         "duration": 0.0,
|         "duration_end": "2014-01-09T11:11:59.772000",
|         "duration_start": "2014-01-09T11:11:59.772000",
|         "groupby": null,
|         "max": 1.0,
|         "min": 1.0,
|         "period": 10,
|         "period_end": "2014-01-09T11:12:08",
|         "period_start": "2014-01-09T11:11:58",
|         "sum": 1.0,
|         "unit": "router"
|     }
| ]
| ```
+-+

* 过滤条件JSON请求样例，groupby

+-+
| GET /v2/meters/router/statistics?groupby=resource_id
+-+
| N/A
+-+

* 过滤条件JSON响应样例，groupby

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "avg": 1.0,
|         "count": 1,
|         "duration": 0.0,
|         "duration_end": "2014-01-09T11:11:59.772000",
|         "duration_start": "2014-01-09T11:11:59.772000",
|         "groupby": {
|             "resource_id": "a67d5d0d-1ad1-4402-99be-192b946dd5cc"
|         },
|         "max": 1.0,
|         "min": 1.0,
|         "period": 0,
|         "period_end": "2014-01-09T11:11:59.772000",
|         "period_start": "2014-01-09T11:11:59.772000",
|         "sum": 1.0,
|         "unit": "router"
|     }
| ]
| ```
+-+

## 告警（Alarm）
### 查询告警（List Alarms）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/alarms?q.op=eq&q.value={value}&q.field={field} | 获取alarm列表

* request filter参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| q.op | string | 只能为eq | No | 操作符
| q.value | string | N/A | No | 值
| q.field | string | 见filed取值表 | No | 查询关键字

field取值表

| 可选值 | Value类型 | 约束 | 备注
|:-------|:----------|:-----|:-----|
| alarm_id | string | N/A | 告警id
| project | string | N/A | 项目id
| user | string | N/A | 用户id
| name | string | N/A | 名称
| enabled | string | 见enabled取值表 | 是否启用
| pagination | int | N/A | 未实现

enabled取值表

| 可选值 | 备注 |
|:-------|:-----|
| t, true, on, y, yes, 1 | 大小写不敏感，取值为True
| 其他 | 取值为False

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/alarms
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "alarm_actions": [],
|         "alarm_id": "7505cd03-dc0f-4539-9906-d019783148fe",
|         "description": "Alarm when instance is eq a avg of 5.0 over 60 seconds",
|         "enabled": true,
|         "insufficient_data_actions": [],
|         "name": "test-member-create-alarm",
|         "ok_actions": [],
|         "project_id": "aebb7f33b7fc4cf486d3a2cdacac8ac1",
|         "repeat_actions": false,
|         "state": "insufficient data",
|         "state_timestamp": "2014-02-08T10:07:03.870000",
|         "threshold_rule": {
|             "comparison_operator": "eq",
|             "evaluation_periods": 1,
|             "meter_name": "instance",
|             "period": 60,
|             "query": [
|                 {
|                     "field": "project_id",
|                     "op": "eq",
|                     "value": "aebb7f33b7fc4cf486d3a2cdacac8ac1"
|                 }
|             ],
|             "statistic": "avg",
|             "threshold": 5.0
|         },
|         "timestamp": "2014-02-08T10:07:03.870000",
|         "type": "threshold",
|         "user_id": "f86eeee169ed48cf892ceac3d5e27a9f"
|     }
| ]
| ```
+-+

* 过滤条件JSON请求样例，enabled

+-+
| GET /v2/alarms?q.op=eq&q.value=true&q.field=enabled
+-+
| N/A
+-+

* 过滤条件JSON响应样例，enabled

由于测试环境中不具有enabled=false的alarm，此处输出为空

+-+
| STATUS CODE 200
+-+
| ```json
| []
| ```
+-+

### 创建告警（Create Alarm）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| POST | /v2/alarms | 创建alarm

* request filter参数

无

* request body参数

**注意，非必选参数未经验证！！**

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| N/A | json dict | N/A | YES | Alarm数据

Alarm结构体

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| name | string | 唯一 | YES | 名称
| type | string | YES | YES | 类型
| threshold_rule | json dict | type=threshold | YES | 阈值规则
| combination_rule | json dict | type=combination | YES | alarm id
| project_id | string | admin可指定 | NO | alarm所属项目
| user_id | string | admin可指定 |NO | alarm所属用户
| description | string | N/A | NO | 描述
| state | string | YES | NO | 状态
| enabled | bool | YES | NO | 是否启用
| alarm_action | string | N/A | NO | 报警时的动作
| ok_action | string | N/A | NO | 正常时的动作
| insufficient_data_action | string | N/A | NO | 数据不正常时的动作
| repeat_actions | bool | N/A | NO | 是否重复执行动作，为真则每次进入状态均执行

type可选值

| 可选值 | 备注 |
|:-------|:-----|
| threshold | 阈值
| combination | 组合

threshold_rule结构体

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| meter_name | string | N/A | YES | 度量名称
| threshold | float | N/A | YES | 阈值
| period | int | N/A | NO | 周期
| evaluation_periods | int | N/A | NO | 计算周期数
| statistic | string | YES | NO | 统计选项
| comparison_operator | string | YES | NO | 比较符
| query | json list | YES | NO | 统计时的过滤项

combination_rule结构体

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| alarm_ids | json list | N/A | YES | alarm id list
| operator | string | YES | NO | 逻辑操作符

alarm_ids结构体

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| N/A | uuid | 必须存在 | YES | alarm id

state可选值

| 可选值 | 备注 |
|:-------|:-----|
| ok | 正常
| alarm | 警报
| insufficient data | 数据不正确

statistic可选值

| 可选值 | 备注 |
|:-------|:-----|
| max | 最大值
| min | 最小值
| avg | 平均值
| sum | 总值
| count | Sample的数量

comparison_operator可选值

| 可选值 | 备注 |
|:-------|:-----|
| lt | 小于
| le | 小于等于
| eq | 等于
| ne | 不等于
| ge | 大于等于
| gt | 大于

operator可选值

| 可选值 | 备注 |
|:-------|:-----|
| and |	alarm同时发生
| or | 其中一个alarm发生

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| POST /v2/alarms
+-+
| ```json
| {
|     "name": "alarm-test",
|     "repeat_actions": false,
|     "threshold_rule": {
|         "meter_name": "instance",
|         "threshold": 10.0
|     },
|     "type": "threshold"
| }
| ```
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| {
|     "alarm_actions": [],
|     "alarm_id": "048341c1-5f41-4d8b-8b1e-a3816a5d9859",
|     "description": "Alarm when instance is eq a avg of 10.0 over 60 seconds",
|     "enabled": true,
|     "insufficient_data_actions": [],
|     "name": "alarm-test",
|     "ok_actions": [],
|     "project_id": "313a8bc21b994e60b93d6fff7c1e0c1b",
|     "repeat_actions": false,
|     "state": "insufficient data",
|     "state_timestamp": "2014-02-11T04:20:02.193000",
|     "threshold_rule": {
|         "comparison_operator": "eq",
|         "evaluation_periods": 1,
|         "meter_name": "instance",
|         "period": 60,
|         "query": [],
|         "statistic": "avg",
|         "threshold": 10.0
|     },
|     "timestamp": "2014-02-11T04:20:02.193000",
|     "type": "threshold",
|     "user_id": "30aee73695744a6096e35fdab25b6766"
| }
| ```

注意，创建同名的alarm将返回：

+-+
| STATUS CODE 400
+-+
| ```json
| {
|     "error_message": {
|         "debuginfo": null,
|         "faultcode": "Client",
|         "faultstring": "Alarm with that name exists"
|     }
| }
| ```
+-+

### 查询告警详情（Show Alarm）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/alarms/{alarm_id} | 获取指定alarm详细信息

* request filter参数

无

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/alarms/7505cd03-dc0f-4539-9906-d019783148fe
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| {
|     "alarm_actions": [],
|     "alarm_id": "7505cd03-dc0f-4539-9906-d019783148fe",
|     "description": "Alarm when instance is eq a avg of 5.0 over 60 seconds",
|     "enabled": true,
|     "insufficient_data_actions": [],
|     "name": "test-member-create-alarm",
|     "ok_actions": [],
|     "project_id": "aebb7f33b7fc4cf486d3a2cdacac8ac1",
|     "repeat_actions": false,
|     "state": "insufficient data",
|     "state_timestamp": "2014-02-08T10:07:03.870000",
|     "threshold_rule": {
|         "comparison_operator": "eq",
|         "evaluation_periods": 1,
|         "meter_name": "instance",
|         "period": 60,
|         "query": [
|             {
|                 "field": "project_id",
|                 "op": "eq",
|                 "value": "aebb7f33b7fc4cf486d3a2cdacac8ac1"
|             }
|         ],
|         "statistic": "avg",
|         "threshold": 5.0
|     },
|     "timestamp": "2014-02-08T10:07:03.870000",
|     "type": "threshold",
|     "user_id": "f86eeee169ed48cf892ceac3d5e27a9f"
| }
| ```
+-+

### 更新告警（Update Alarm）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| PUT | /v2/alarms/{alarm_id} | 修改指定alarm信息

* request filter参数

无

* request body参数

见创建告警章节

* response body参数

见创建告警章节

* 相关配置

* JSON请求样例

+-+
| PUT /v2/alarms/7505cd03-dc0f-4539-9906-d019783148fe
+-+
| ```json
| {
|     "name": "test-member-create-alarm",
|     "threshold_rule": {
|         "meter_name": "instance",
|         "threshold": 10.0
|     },
|     "type": "threshold"
| }
| ```
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| {
|     "alarm_actions": [],
|     "alarm_id": "7505cd03-dc0f-4539-9906-d019783148fe",
|     "description": "Alarm when instance is eq a avg of 10.0 over 60 seconds",
|     "enabled": true,
|     "insufficient_data_actions": [],
|     "name": "test-member-create-alarm",
|     "ok_actions": [],
|     "project_id": "aebb7f33b7fc4cf486d3a2cdacac8ac1",
|     "repeat_actions": false,
|     "state": "insufficient data",
|     "state_timestamp": "2014-02-15T08:02:22.189000",
|     "threshold_rule": {
|         "comparison_operator": "eq",
|         "evaluation_periods": 1,
|         "meter_name": "instance",
|         "period": 60,
|         "query": [
|             {
|                 "field": "project_id",
|                 "op": "eq",
|                 "value": "aebb7f33b7fc4cf486d3a2cdacac8ac1"
|             }
|         ],
|         "statistic": "avg",
|         "threshold": 10.0
|     },
|     "timestamp": "2014-02-15T16:41:03.528000",
|     "type": "threshold",
|     "user_id": "f86eeee169ed48cf892ceac3d5e27a9f"
| }
| ```
+-+

### 删除告警（Delete Alarm）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| DELETE | /v2/alarms/{alarm_id} | 删除指定alarm

* request filter参数

无

* response body参数

无

* 相关配置

* JSON请求样例

+-+
| DELETE /v2/alarms/c4278318-0572-45b6-96f8-e321cf44f817
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 204
+-+
| N/A
+-+

### 查询告警状态（Get Alarm State）

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| GET | /v2/alarms/{alarm_id}/state | 获取指定alarm状态

* request filter参数

无

* request body参数

无

* response body参数

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| N/A | string | N/A | YES | 告警状态

* 相关配置

* JSON请求样例

+-+
| GET /v2/alarms/7505cd03-dc0f-4539-9906-d019783148fe/state
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| "insufficient data"
| ```
+-+

### 更新告警状态(Set Alarm State)

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| PUT | /v2/alarms/{alarm_id}/state | 更新指定alarm状态

* request filter参数

无

* request body参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| N/A | string | YES | YES | 告警状态

可选值

| 可选值 | 备注 |
|:-------|:-----|
| ok | 正常
| alarm | 警报
| insufficient data | 数据不正确

大小写敏感，提交错误的状态将会返回400 Bad Request

+-+
| STATUS CODE 400
+-+
| ```json
| {
|     "error_message": {
|         "debuginfo": null,
|         "faultcode": "Client",
|         "faultstring": "state invalid"
|     }
| }
| ```
+-+

* response body参数

| 参数名 | 参数类型 | 约束 | 必选 | 备注 |
|:-------|:---------|:-----|:-----|:-----|
| N/A | string | N/A | YES | 告警状态

* 相关配置

* JSON请求样例

+-+
| PUT /v2/alarms/7505cd03-dc0f-4539-9906-d019783148fe/state
+-+
| ```json
| "ok"
| ```
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| "ok"
| ```
+-+

### 查询告警历史信息(Show Alarm History)

| REST VERB | URI | DESCRIPTION |
|:----------|:----|:------------|
| PUT | /v2/alarms/{alarm_id}/history | 获取指定alarm历史信息

history是alarm的变动记录，对应模型AlarmChange，对应数据库表alarm_history。

* request filter参数

未知，从代码角度能看到支持过滤选项，但是经过试验又总是提示state invalid，即使过滤条件是state也如此。

* request body参数

无

* response body参数

待更新

* 相关配置

* JSON请求样例

+-+
| GET /v2/alarms/7505cd03-dc0f-4539-9906-d019783148fe/history
+-+
| N/A
+-+

* JSON响应样例

+-+
| STATUS CODE 200
+-+
| ```json
| [
|     {
|         "alarm_id": "7505cd03-dc0f-4539-9906-d019783148fe",
|         "detail": "{\"alarm_actions\": [], \"user_id\": \"f86eeee169ed48cf892ceac3d5e27a9f\", \"name\": \"test-member-create-alarm\", \"timestamp\": \"2014-02-08T10:07:03.870024\", \"enabled\": true, \"state_timestamp\": \"2014-02-08T10:07:03.870024\", \"rule\": {\"meter_name\": \"instance\", \"evaluation_periods\": 1, \"period\": 60, \"statistic\": \"avg\", \"threshold\": 5.0, \"query\": [{\"field\": \"project_id\", \"value\": \"aebb7f33b7fc4cf486d3a2cdacac8ac1\", \"op\": \"eq\"}], \"comparison_operator\": \"eq\"}, \"alarm_id\": \"7505cd03-dc0f-4539-9906-d019783148fe\", \"state\": \"insufficient data\", \"insufficient_data_actions\": [], \"repeat_actions\": false, \"ok_actions\": [], \"project_id\": \"aebb7f33b7fc4cf486d3a2cdacac8ac1\", \"type\": \"threshold\", \"description\": \"Alarm when instance is eq a avg of 5.0 over 60 seconds\"}",
|         "event_id": "758e4f1d-cf0a-4b19-b715-856528be7aba",
|         "on_behalf_of": "aebb7f33b7fc4cf486d3a2cdacac8ac1",
|         "project_id": "aebb7f33b7fc4cf486d3a2cdacac8ac1",
|         "timestamp": "2014-02-08T10:07:03.870000",
|         "type": "creation",
|         "user_id": "f86eeee169ed48cf892ceac3d5e27a9f"
|     }
| ]
| ```
+-+
