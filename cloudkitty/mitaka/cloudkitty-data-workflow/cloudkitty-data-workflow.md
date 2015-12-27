# Basic of CloudKitty

## Rating as a Service

CloudKitty is a Rating As A Service project aimed at translating Ceilometer metrics to prices.[^1]

\begin{center}
\includegraphics[width=3in]{images/openstack-service-level.jpg}
\end{center}

[^1]: http://docs.openstack.org/developer/cloudkitty

## Modules

    * API
    * Data Collection
    * Rating Processing
    * Storage
    * Report Writer

Advantages: Highly modular, support extensions/drivers

## Processes

* Processes
    * cloudkitty-api: API, Storage
    * cloudkitty-processor: Data Collection, Rating Processing, Storage
* Disadvantages:
    * API doesn't support Apache mod_wsgi
    * processor doesn't have HA

## Architecture

\begin{center}
\includegraphics[width=3.5in]{images/cloudkitty-architecture.jpg} \\
http://www.slideshare.net/objectiflibre/cloudk
\end{center}

## API

| Functionality Group | Usage or Rating | API Count |
|:-|:-|:-|
| API Versions | X | 1 |
| Collector | X | 7 |
| Rating | Rating | 5 |
| Report | Rating | 2 |
| HashMap | Rating | 21 |
| PyScripts | Rating |5 |
| Storage | Usage | 1 |

Disadvantage: Only 1 API provides all the usage data:

* Can filter by tenant, service, time range
* Cannot filter by resource
* No usage aggregation

## Supported Services

| Service | Ceilometer Meter |
|:--------|:-----------------|
| compute | instance |
| image | image.size |
| volume | volume.size |
| network.bw.in | network.incoming.bytes |
| network.bw.out | network.outgoing.bytes |
| network.floating | ip.floating |

* Advantage: services can be configured
* Disadvantage:  hard-coded, new service is not plugable

# CloudKitty Data Workflow

## Main Engine: orchestrator.py

    for tenant in tenants:
        for service in services:
            collect data
            wrap data
            for processor in processors:
                process data
            store data to database
        update tenant status

## Collect Data

* Collector
    * Ceilometer
    * Meta
* Transformer
    * Ceilometer
    * CloudKitty

## Collect Data Example: compute

    ceilometer.statistics.get(meter=instance, groupby=resource_id)
    for resource_id in resource_ids:
        resource = ceilometer.resources.get('compute', resource_id)
        resource = transformer.ceilometer.strip_resource_data(resource)
        resource = transformer.cloudkitty.format_item(resource)
        resources.append(resource)
    return ftransformer.cldoukitty.format_service('compute', resources)

Performance risk: http request inside a big loop!

## Collect Data Example: compute - Cont.

Ceilometer transformer strip_resource_data('compute', data) keeps attributes:

    * name
    * flavor
    * vcpus
    * memory
    * image_id
    * availability_zone
    * all user_metadata

Attributes list is hard-coded

## Collect Data Example: compute - Cont.

After Ceilometer Transformer:

    {
        "availability_zone": "nova",
        "flavor": "m1.small",
        "image_id": "f83a90d0-6048-40c9-9c11-43b1bcc557ab",
        "instance_id": "eae257fa-abf6-4c4d-9d7e-4d035eea4eb3",
        "memory": "2048",
        "metadata": {},
        "name": "vm-02",
        "project_id": "227ce96c971f4426a6def2ec524c7922",
        "user_id": "6ec1989b80f945389fb97e26c1b31dc5",
        "vcpus": "1"
    }

## Collect Data Example: compute - Cont.

After CloudKitty Transformer format_item():

    {
        "desc": Ceilometer Transformer Result,
        "vol": {
            "qty": 1,
            "unit": "instance"
        }
    }

## Collect Data Example: compute - Cont.

After CloudKitty Transformer format_service():

    {
        "compute": [
            {
                "desc": Ceilometer Transformer Result,
                "vol": {
                    "qty": 1,
                    "unit": "instance"
                }
            }
        ]
    }

## Wrap Data  Example: compute

orchestrator.Worker._collect(), add period info:

    [
        {
            "period": {
                "begin": 1451319060,
                "end": 1451319120
            },
            "usage": {
                CloudKitty Transformer Result
            }
        }
    ]

## Rating

Rating modules - the processors, consume data coming from collector (after wrapped by main engine)

* noop
* hashmap
* pyscripts

Sort by priority of modules

## Rating Example: compute

Add 'rating' attribute for each resource if not existent, i.e. after:

    [{
        "period": { "begin": 1451319780, "end": 1451319840 },
        "usage": {
            "compute": [{
                "desc": Ceilometer Transformer Result,
                "rating": {
                    "price": 0
                },
                "vol": { "qty": 1, "unit": "instance" }
            }]
        }
    }]

## Rating HashMap

* group: divide rating calculation (global for services)
* service: service level mappings and thresholds
* field: instance level mappings and thresholds
* mapping: rating by resource metadata (i.e. flavor)
* threshold: rating by resource usage quantity (i.e. network bytes)

## Rating PySricpts

    import decimal
    
    for data in datas:
        for service, resources in data['usage'].items():
            if service == 'compute':
                for resource in resources:
                    if resource['desc'].get('flavor') == 'm1.nano':
                        resource['rating'] = {
                            'price': decimal.Decimal(1.0)}

## Persist Usage Data

* store data (comes from last processor) to SQL
* each row is instance level usage and rating price for a configured time period
* no aggregation, raw data

## MySQL Table Desc: rated_data_frames


    mysql> desc cloudkitty.rated_data_frames;
    +-----------+---------------+------+-----+---------+----------------+
    | Field     | Type          | Null | Key | Default | Extra          |
    +-----------+---------------+------+-----+---------+----------------+
    | id        | int(11)       | NO   | PRI | NULL    | auto_increment |
    | begin     | datetime      | NO   |     | NULL    |                |
    | end       | datetime      | NO   |     | NULL    |                |
    | unit      | varchar(255)  | NO   |     | NULL    |                |
    | qty       | decimal(10,0) | NO   |     | NULL    |                |
    | res_type  | varchar(255)  | NO   |     | NULL    |                |
    | rate      | float         | NO   |     | NULL    |                |
    | desc      | text          | NO   |     | NULL    |                |
    | tenant_id | varchar(32)   | YES  |     | NULL    |                |
    +-----------+---------------+------+-----+---------+----------------+

# Comparing to Moneta

## Usage

Moneta Wins:

* Moneta can aggregate by hour/day/month, CloudKitty cannot
* Moneta can aggregate by tenant, CloudKitty cannot
* Moneta can aggregate by instance, CloudKitty cannot

CloudKitty Wins:

* CloudKitty can get all the usage data points, Moneta cannot

Draw:

* Both can filter by tenant, service/metric, time range

## Price

CloudKitty Wins:

* CloudKitty enables fully customized rating rules and scripts, Moneta cannot
* CloudKitty can get total price by tenant and service, Moneta offloads to third-par

Draw:

* CloudKitty can generate report files [^2] for third-par, Moneta supplies API for third-par

[^2]: the file generated by CloudKitty is raw data

## Development Activity

CloudKitty (mainly by Stephane Albert @ Objectif Libre):

\begin{center}
\includegraphics[width=4in]{images/ck-dev-heat.jpg}
\end{center}

Ceilometer:

\begin{center}
\includegraphics[width=4in]{images/cm-dev-heat.jpg}
\end{center}

Nova:

\begin{center}
\includegraphics[width=4in]{images/nova-dev-heat.jpg}
\end{center}

## CloudKitty Support

* Good:
    * integrated with Horizon
    * Supports devstack
    * has full API documents
    * weekly irc meeting
* Bad:
    * Lack of example [^3]
    * No use case, no user guide
    * Lack of code comment
    * Buggy

[^3]: has several short video demos, but doesn't explain why doing so and what the effect

##

\begin{center}
\vspace*{\fill}
\Huge{QUESTIONS ?}
\vspace*{\fill}
\end{center}
