### Disclaimer:
#### This is a working title of a "Configuring bykstack"
-----------------------------------------------------------------------------

### About
This document covers how and what to configure before starting the installation 

#### Bykstack structure

```
── chat-widget
│   ├── cert.crt
│   ├── index.html
│   ├── key.key
│   └── nginx.conf
├── customer-support
│   ├── cert.crt
│   ├── env-config.js
│   ├── key.key
│   └── nginx.conf
├── dmapper
│   ├── cert.crt
│   ├── key.key
│   └── server.xml
├── docker-compose.yml
├── generate-certs.py
├── logstash
│   ├── logstash.conf
│   └── logstash.yml
├── monitor
│   ├── cert.crt
│   ├── env-config.js
│   ├── key.key
│   └── nginx.conf
├── opensearch
│   ├── assets
│   │   ├── buerokratt-blue.svg
│   │   ├── buerokratt-white.svg
│   │   └── favicon.ico
│   ├── config
│   │   ├── admin-key.pem
│   │   ├── admin.pem
│   │   ├── cert.crt
│   │   ├── client-key.pem
│   │   ├── client.pem
│   │   ├── generate-certificates.sh
│   │   ├── key.key
│   │   ├── node1-key.pem
│   │   ├── node1.pem
│   │   ├── root-ca-key.pem
│   │   ├── root-ca.pem
│   │   └── root-ca.srl
│   ├── dashboards.yml
│   ├── jvm.options
│   ├── opensearch.yml
│   └── securityconfig
│       ├── config.yml
│       ├── internal_users.yml
│       ├── roles.yml
│       └── roles_mapping.yml
├── resql
│   ├── cert.crt
│   ├── key.key
│   └── server.xml
├── ruuter
│   ├── cert.crt
│   ├── key.key
│   ├── private.urls.docker.json
│   ├── public.urls.docker.json
│   └── server.xml
└── tim
    ├── README.md
    ├── cert.crt
    ├── docker-compose.yml
    ├── jwtkeystore.jks
    ├── key.key
    └── server.xml

```
