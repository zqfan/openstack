os ubuntu 16.04, using devstack to deploy openstack mitaka

1. create /etc/neutron/metering_agent.ini
2. run process ``/usr/bin/python /usr/local/bin/neutron-metering-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/metering_agent.ini`` in stack screen
3. create meter label for demo project: ``neutron meter-label-create --tenant-id `openstack project show demo -f value -c id` demo-l3-meter``


related refs:

* https://bugs.launchpad.net/openstack-manuals/+bug/1318604
* http://docs.openstack.org/admin-guide/networking-adv-config.html
* http://docs.openstack.org/admin-guide/networking-adv-features.html
* https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/5/html/Cloud_Administrator_Guide/section_networking-advanced-config.html
