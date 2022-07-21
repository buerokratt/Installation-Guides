# Bürokratt
Describe what it is and what it is used for
Sort of project overview

### Components
* [private-ruuter ??](https://github.com/buerokratt/Ruuter)??
* [public-ruuter ??](https://github.com/buerokratt/Ruuter)??
* [DataMapper](https://github.com/buerokratt/DataMapper)
* widget
* customer-service
* [TIM](https://github.com/buerokratt/TIM)
* [RESQL](https://github.com/buerokratt/RESQL)
* bot
* action-server
* Client side log collecting

### Images in Dockerhub
* https://hub.docker.com/r/riaee/byk-users-db
* https://hub.docker.com/r/riaee/byk-ruuter
* https://hub.docker.com/r/riaee/byk-chatbot-public-ruuter
* https://hub.docker.com/r/riaee/byk-chatbot-private-ruuter
* https://hub.docker.com/r/riaee/byk-tim
* https://hub.docker.com/r/riaee/byk-resql
* https://hub.docker.com/r/riaee/byk-dmapper
* https://hub.docker.com/r/riaee/byk-chat-widget
* https://hub.docker.com/r/riaee/byk-customer-service

## Table of Contents

- [Installing](#installing)
  - [Resource requirements](#approximate-resource-requirements)
  - [Overview of the system](#overview-of-traffic-flow-on-the-system)
  - [Setting up DB](#databases)
- [Using](#using)
- [Services](#services)
- [License](#license)
- [How to Contribute](#how-to-contribute)

## Installing

As the system can be grouped into 3 parts also 3 machines are needed:

* Bykstack - setting up instructions are [here](./bykstack/)
* Bot - setting up instructions are [here](./bot/)
* Training-bot - setting up instructions are [here](./bot_training/)

### Approximate resource requirements
- Bot ~3GB RAM and 4CPU
- Bykstack ~10GB RAM and 7CPU
- Training-bot ~3GB RAM and 4CPU

Additional ressources are needed for SQL database and traffic forwarder/reverse-proxy

## Exposing to the internet

Only selected components need traffic from internet:
- Bykstack:
  - Public-ruuter
  - Private-ruuter
  - Tim
  - Widget
  - Customer-support

### Overview of traffic flow on the system
![Overview-Light](./images/overview.light.editable.png#gh-light-mode-only)![Overview-Dark](./images/overview.dark.editable.png#gh-dark-mode-only)

## Databases

#### SQL Databases
2 components are using PostgreSQL databases: TIM and RESQL.

Component **TIM** database gets set up on first run automatically. 

Users database, used by **RESQL**, needs some manual steps:
* Creating DB structure
```
docker run -it --network=bykstack PLACEHOLDER USERS_DB_SETUP_IMAGE bash
liquibase --url=jdbc:postgresql://users-db:5432/byk?user=byk --password=PLACEHOLDER USERS_DB_PASSWORD --changelog-file=/master.yml update
```
* Adding configuration

```
docker run -it --network=bykstack ubuntu:latest bash
apt-get -y update && apt-get -y install postgresql-client
psql -d byk -U byk -h users-db -p 5432
insert into configuration(key, value) values ('bot_institution_id', 'PLACEHOLDER BOT_NAME');
CREATE EXTENSION hstore;
```

# Using
Describe how to use running software

# Client side log collecting
Work in Progress!!  
Client infrastructure will contain a log collecting and shipping modules. 
Promtail will collect, transform and ships logs to Loki, which will push logs to central logging system that will pull those logs, depending on the interval set up in that system.
Client side log collection ``` docker-compose ``` will be shown in examples (`logs_shipping.yml`)

Loki configuration (`loki-config.yml`)
```
---
server:
  http_listen_port: 3100
memberlist:
  join_members:
    - loki:7946
schema_config:
  configs:
    - from: DATE YYYY-MM-DD
      store: boltdb-shipper
      object_store: s3
      schema: v11
      index:
        prefix: index_
        period: 24h
common:
  path_prefix: /PREFIXNAME
  replication_factor: 1
  storage:
    s3:
      endpoint: minio:9000
      insecure: true
      bucketnames: loki-data
      access_key_id: USERNAME
      secret_access_key: PASSWORD
      s3forcepathstyle: true
  ring:
    kvstore:
      store: memberlist
ruler:
  storage:
    s3:
      bucketnames: loki-ruler
 ```

Promtail configuration (`promtail-config.yml`)
```
---
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://gateway:3100/loki/api/v1/push
    tenant_id: tenant1

scrape_configs:
  - job_name: flog_scrape 
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
pipeline_stages:
  - json:
      expressions:
        output: log
        stream: stream
        attrs:
  - json:
      expressions:
        tag:
      source: attrs
  - regex:
      expression: (?P<image_name>(?:[^|]*[^|])).(?P<container_name>(?:[^|]*[^|])).(?P<image_id>(?:[^|]*[^|])).(?P<container_id>(?:[^|]*[^|]))
      source: tag
  - timestamp:
      format: RFC3339Nano
      source: time
  - labels:
      tag:
      stream:
      image_name:
      container_name:
      image_id:
      container_id:
  - output:
      source: output
```




## Services

More in-depth overview of Bureokratt's services is [here](./functionalities/readme.md)

## License

[MIT](./LICENSE)

## Contributing/Credits

Give thanks and credits for contributors

## How to Contribute
