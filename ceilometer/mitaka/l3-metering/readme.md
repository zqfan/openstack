os ubuntu 16.04, using devstack to deploy openstack mitaka

0. create a vm and associate a floating ip to it, for i.e. 172.24.4.3
0. create meter label for demo project: ``neutron meter-label-create --tenant-id `openstack project show demo -f value -c id` demo-l3-meter``
0. create meter rule: ``neutron meter-label-rule-create demo-l3-meter 172.24.4.0/24 --direction ingress``, note it should be a range rather than an individual ip addr, which means 172.24.4.3/32 doesn't work
0. create meter rule: ``neutron meter-label-rule-create demo-l3-meter 172.24.4.0/24 --direction egress``
0. query sample in ceilometer: ``ceilometer sample-list -m bandwidth -q metadata.tenant_id=`openstack project show demo -f value -c id```, note that ceilometer only record bytes as value by default.

neutron-metering-agent collects data per 30s for each meter-label and report to AMQP per 5m by default. a sample of bandwidth is like:

~~~json
{
    "counter_name": "bandwidth",
    "counter_type": "delta",
    "counter_unit": "B",
    "counter_volume": 0.0,
    "message_id": "fbbd39fe-cf32-4511-8876-31d6125b30b6",
    "project_id": "96334dea08144e1b8cf7c4b1896d9863",
    "recorded_at": "2016-11-03T17:00:04.322150",
    "resource_id": "8343bec6-fcec-40d4-87a3-37701c0e3689",
    "resource_metadata": {
        "bytes": "0",
        "event_type": "l3.meter",
        "first_update": "1478192194",
        "host": "metering.BJWS",
        "label_id": "9c236f28-4f27-4bc0-921b-6336770c4984",
        "last_update": "1478192404",
        "pkts": "0",
        "tenant_id": "96334dea08144e1b8cf7c4b1896d9863",
        "time": "210"
    },
    "source": "openstack",
    "timestamp": "2016-11-03T17:00:04.192928",
    "user_id": null
}
~~~

related refs:

* https://bugs.launchpad.net/openstack-manuals/+bug/1318604
* http://docs.openstack.org/admin-guide/networking-adv-config.html
* http://docs.openstack.org/admin-guide/networking-adv-features.html
* https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/5/html/Cloud_Administrator_Guide/section_networking-advanced-config.html
