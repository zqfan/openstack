"""A script to calculate monasca data size. CAUTION: It is very time consuming in a real environment!"""
import datetime
import os

from monascaclient import client
from monascaclient import ksclient

auth_url = os.environ.get('OS_AUTH_URL')
username = os.environ.get('OS_USERNAME')
password = os.environ.get('OS_PASSWORD')
project_name = os.environ.get('OS_PROJECT_NAME')


def mon_client():
    kwargs = {
        'username': username,
        'password': password,
        'auth_url': auth_url,
        'project_name' : project_name,
        'endpoint_type': 'adminURL'  # publicURL is default bu may require https and slower than adminURL
    }

    _ksclient = ksclient.KSClient(**kwargs)
    kwargs = {'token': _ksclient.token}
    return client.Client('2_0', _ksclient.monasca_url, **kwargs)

m = mon_client().metrics

unique_metrics = {}
for metric in m.list_names():
    unique_metrics[metric['name']] = 1

start = datetime.datetime.now() - datetime.timedelta(days=60)
aggregate = {}
for metric in sorted(unique_metrics.keys()):
    print metric
    statistics = m.list_statistics(name=metric,
                                   merge_metrics="True",
                                   statistics="count",
                                   period="1000000000",
                                   start_time=start.isoformat())
    for stat in statistics:
        key = stat['name']
        count = stat['statistics'][0][1]
        print "   {} -> {}".format(key, count)
        if key in aggregate:
            aggregate[key] += count
        else:
            aggregate[key] = count

print "total measurements = {}".format(sum(aggregate.values()))

metric_count = 0
for metric in sorted(unique_metrics.keys()):
    metric_count += len(m.list(name=metric))

print "total metrics =", metric_count
