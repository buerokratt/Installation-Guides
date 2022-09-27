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
#### CookieDomain 
Cookie domain determines from which domain traffic is allowed into Buerokratt system. Top level domain is not recommended due to security concerns. And in the other hand defining domain and sub domains too tightly disables traffic between chat-widgets on different sub domains.

##### server.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<Server port="8005" shutdown="SHUTDOWN">
    <Listener className="org.apache.catalina.startup.VersionLoggerListener"/>
    <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on"/>
    <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener"/>
    <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener"/>
    <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener"/>
    <GlobalNamingResources>
        <Resource name="UserDatabase" auth="Container"
                  type="org.apache.catalina.UserDatabase"
                  description="User database that can be updated and saved"
                  factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                  pathname="conf/tomcat-users.xml"/>
    </GlobalNamingResources>
    <Service name="Catalina">
        <Connector port="8443"
                   protocol="org.apache.coyote.http11.Http11NioProtocol"
                   clientAuth="false"
                   sslProtocol="TLSv1.2, TLSv1.3"
                   SSLEnabled="true"
                   maxThreads="150"
                   scheme="https"
                   secure="true"
                   SSLCertificateFile="${catalina.base}/conf/cert.crt"
                   SSLCertificateKeyFile="${catalina.base}/conf/key.key"
        />
        <Engine name="Catalina" defaultHost="localhost">
            <Realm className="org.apache.catalina.realm.LockOutRealm">
                <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
                       resourceName="UserDatabase"/>
            </Realm>

            <Host name="localhost" appBase="webapps"
                  unpackWARs="true" autoDeploy="true">
                <Valve className="org.apache.catalina.valves.ErrorReportValve" showReport="false" showServerInfo="false" />
                <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
                       prefix="localhost_access_log" suffix=".txt"
                       pattern="%h %l %u %t &quot;%r&quot; %s %b"/>

            </Host>
        </Engine>
    </Service>
</Server>
```
