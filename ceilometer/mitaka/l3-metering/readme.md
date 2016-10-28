os ubuntu 16.04, using devstack to deploy openstack mitaka

1. create /etc/neutron/metering_agent.ini
2. run process ``/usr/bin/python /usr/local/bin/neutron-metering-agent --config-file /etc/neutron/neutron.conf --config-file /etc/neutron/metering_agent.ini`` in stack screen
3. create meter label for demo project: ``neutron meter-label-create --tenant-id `openstack project show demo -f value -c id` demo-l3-meter``
