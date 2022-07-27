# bykstack

Stack of components handling chat.

## Table of Contents

- [List of dependencies](#list-of-dependencies)
- [Installing](#installing)
  - [public-ruuter](#private-ruuter)
  - [private-ruuter](#public-ruuter)
  - [dmapper](#test-bot)
  - [widget](#test-bot)
  - [customer-service](#test-bot)
  - [tim](#test-bot)
  - [resql](#test-bot)
  - [monitoring-module](#monitoring-module)
- [License](#license)
- [How to Contribute](#how-to-contribute)

## List of dependencies

- Docker with compose plugin
- ssh server
- PostgreSQL DB system
- [TARA](https://www.ria.ee/en/state-information-system/eid/partners.html#tara) contract
- Reverse proxy

## Installing

The Bykstack consists of 11 containers. They should be in one docker network. Example docker-compose file is [here](./examples/docker-compose.yml).

**All** components need encrypted traffic between reverse-proxy and its endpoint. Please generate key-cert pairs for every component separately.
### Logging levels

At the moment all components are developed using [Spring](https://spring.io/) framework. Logging level are `ERROR` `WARN` `INFO` `DEBUG` `TRACE`

### CookieDomain

Cookie domain determines from which domain traffic is allowed into Buerokratt system. Top level domain is not recommended due to security concerns. And in the other hand defining domain and sub domains too tightly disables traffic between chat-widgets on different sub domains.

### server.xml

Some components run on Tomcat server and need configuration.
Example server.xml file:
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

## Private-ruuter
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Update `urls.env.json` url-s linking to your setups components.
For example:
```json
{
  "dmapper_url": "https://byk-dmapper:8443",
  "ruuter_url": "http://localhost:8443",
  "tim_url": "https://byk-tim:8443",
  "resql_url": "https://byk-resql:8443",
  "bot_url": "http://PLACEHOLDER BOT_IP:5005",
  "training_url": "PLACEHOLDER TRAINIG_BOT",
  "training_user": "PLACEHOLDER TRAINING_BOT_USERNAME",
  "training_prv_key": "PLACEHOLDER TRAINIG_BOT_PRIVATE_SSH_KEY_PATH",
  "training_bot_directory_name": "PLACEHOLDER TRAINING_DATA_DIRECTORY",
  "gazetteer_url":"https://inaadress.maaamet.ee/inaadress",
  "publicapi_url": "https://publicapi.envir.ee/v1/combinedWeatherData",
  "ilmmicroservice_url": "https://ilmmicroservice.envir.ee/api/forecasts"
}
```

### Running the container

In order to create container from image bring it up like so:
```
docker run \
    -p 8443:8443 \
    -e legacy-portal-integration.sessionCookieDomain=PLACEHOLDER YOUR_DOMAIN \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -e ruuter.cookie.sameSitePolicy=None \
    -e ruuter.cors.allowedOrigins=PLACEHOLDER ALLOWED ORIGINS \
    -e headers.contentSecurityPolicy= \
    -e maxRequestSizeBytes=10000000000 \
    -e incoming.request.external.validation.enabled=false \ 
    -e incoming.request.external.validation.endpoint= \
    -e verify.requested.method.type=false \
    -e allowed.requested.method.types=POST \
    -e default.requested.method.type=POST \
    -e requested.method.type.error.http.response.code=200 \
    -e csrf.enabled=false \
    -e csrf.tim_userinfo_url= \
    -e csrf.ruuter_services_whitelist= \
    -e ip-whitelist.routes[0].ips[0]=127.0.0.1 \
    -e ip-whitelist.routes[0].patterns[0]=/functions/* \
    -e ip-whitelist.routes[1].ips[0]=127.0.0.1 \
    -e ip-whitelist.routes[1].patterns[0]=/get-location-coordinates \
    -e ip-whitelist.routes[1].patterns[1]=/get-weather-data \
    -e ip-whitelist.routes[1].patterns[2]=/get-weather-station-id \
    -e ip-whitelist.routes[1].patterns[3]=/get-weather \
    -e ip-whitelist.routes[1].patterns[4]=/param_string_length \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v /path_to/urls.env.json:/usr/local/tomcat/urls.env.json \
    -v /path_to/cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v /path_to/key.key:/usr/local/tomcat/conf/key.key \
    -v /path_to/location/of/private/ssh/key:/root/.ssh/id_training \
    PLACEHOLDER:IMAGE_NAME
```
## Public-ruuter
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Update `urls.env.json` url-s linking to your setups components.
For example:
```json
{
  "dmapper_url": "https://byk-dmapper:8443",
  "ruuter_url": "http://localhost:8443",
  "tim_url": "https://byk-tim:8443",
  "resql_url": "https://byk-resql:8443",
  "bot_url": "http://PLACEHOLDER BOT_IP:5005",
  "training_url": "PLACEHOLDER TRAINIG_BOT",
  "training_user": "PLACEHOLDER TRAINING_BOT_USERNAME",
  "training_prv_key": "PLACEHOLDER TRAINIG_BOT_PRIVATE_SSH_KEY_PATH",
  "training_bot_directory_name": "PLACEHOLDER TRAINING_DATA_DIRECTORY",
  "gazetteer_url":"https://inaadress.maaamet.ee/inaadress",
  "publicapi_url": "https://publicapi.envir.ee/v1/combinedWeatherData",
  "ilmmicroservice_url": "https://ilmmicroservice.envir.ee/api/forecasts"
}

```
### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 8443:8443 \
    -e legacy-portal-integration.sessionCookieDomain=PLACEHOLDER YOUR_DOMAIN \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -e csrf.enabled=false \
    -e csrf.tim_userinfo_url= \
    -e csrf.ruuter_services_whitelist= \
    -e allowed.requested.method.types=POST \
    -e ruuter.cors.allowedOrigins=PLACEHOLDER ALLOWED ORIGINS \
    -e maxRequestSizeBytes=10000000000 \
    -e default.requested.method.type=POST \
    -e incoming.request.external.validation.enabled=false \
    -e requested.method.type.error.http.response.code=200 \
    -e verify.requested.method.type=false \
    -e incoming.request.external.validation.endpoint= \
    -e headers.contentSecurityPolicy= \
    -v /path_to/server.xml:/usr/local/tomcat/conf/server.xml \
    -v /path_to/urls.env.json:/usr/local/tomcat/urls.env.json \
    -v /path_to/cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v /path_to/key.key:/usr/local/tomcat/conf/key.key \
    PLACEHOLDER:IMAGE_NAME
```

## DataMapper
Mount certificates into container as `/usr/local/tomcat/conf/tls.crt` and `/usr/local/tomcat/conf/tls.key`

### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 8081:8443 \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./urls.env.json:/usr/local/tomcat/urls.env.json \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/tls.key \
    PLACEHOLDER:IMAGE_NAME
```

## Widget
Mount certificates into container as `/etc/tls/tls.crt` and `/etc/tls/tls.key`

Update `index.html` url-s linking to your setups components.
Where `RUUTER_API_URL` is URL pointing to the Public-ruuter, `TIM_AUTHENTICATION_URL` is URL pointing to the TIM and the URL of the page wher widget is installed into, and:
* `OFFICE_HOURS`: If this variable is added, widget will be hidden when not in defined work hours. If this variable is not added, the widget will always be displayed
  * `TIMEZONE`: Used for comparing the following variables against a specific timezone.
  * `BEGIN`: Beginning of office hours. If current time is before this hour (24H), the widget will not be displayed
  * `END`: End of office hours. If current time is after this hour (24H), the widget will not be displayed
  * `DAYS`: List of days in numbers, where 1=monday, 2=tuesday, 3=wednesday... If current day is in the list of days, the widget will be displayed according to `BEGIN` and `END` times.

For example:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Title</title>
</head>
<body>
<div id="byk-va"></div>
<script>
  window._env_ = {
    RUUTER_API_URL: 'https://PLACEHOLDER PUBLIC-RUUTER_URL',
    TIM_AUTHENTICATION_URL: 'https://PLACEHOLDER TIM_URL/oauth2/authorization/tara?callback_url=https://PLACEHOLDER URL_WHERE_TO_WIDGET_IS_INSTALLED',
    OFFICE_HOURS: {
      TIMEZONE: 'Europe/Tallinn',
      BEGIN: 0,
      END: 24,
      DAYS: [1, 2, 3, 4, 5],
    },
  };
</script>
<script id="script-bundle" type="text/javascript" src="./widget_bundle.js" crossorigin=""></script>
</body>
<style>
  .background {
    background: #004d40;
    width: 100vw;
    height: 100vh;
  }
</style>
</html>

```
In the file `nginx.conf` update header adding according to your setup so that all pages where the widget is installed are allowed to access. If wiget is installed into multiple pages add define extra line 

For example:
```
server {
    server_name localhost;
    listen 443 ssl;
    ssl_certificate /etc/tls/tls.crt;
    ssl_certificate_key /etc/tls/tls.key;

    server_tokens off;
    add_header 'Access-Control-Allow-Origin' 'https://PLACEHOLDER FIRST_PAGE_WITH_WIDGET' always;
    add_header 'Access-Control-Allow-Origin' 'https://PLACEHOLDER SECOND_PAGE_WITH_WIDGET' always;

    location / {
        root /usr/share/nginx/html/widget;
        index index.html;
    }

    location /status {
        access_log off;
        default_type text/plain;
        add_header Content-Type text/plain;
        return 200 "alive";
    }

    location ~* \.(js|jpg|png|css)$ {
        root /usr/share/nginx/html/widget;
    }
}

server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_uri;
}
```
### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 3000:443 \
    -v ./nginx.conf:/etc/nginx/conf.d/default.conf \
    -v ./index.html:/usr/share/nginx/html/widget/index.html \
    -v ./cert.crt:/etc/tls/tls.crt \
    -v ./key.key:/etc/tls/tls.key \
    PLACEHOLDER:IMAGE_NAME 
```

## Customer-service

Mount certificates into container as `/etc/ssl/certs/cert.crt` and `/etc/ssl/certs/key.key`

Update `env-config.js` url-s linking to your setups components.
For example:
```
{
    RUUTER_API_URL: 'https://PLACEHOLDER PRIVATE_RUUTER_URL',
    TIM_API_URL: 'https://PLACEHOLDER TIM_URL',
    TARA_REDIRECT_URL: 'https://PLACEHOLDER TIM_URL/oauth2/authorization/tara?callback_url=https://PLACEHOLDER CUSTOMER_SERVICE_URL/auth/callback',
    MONITORING_URL: https://PLACEHOLDER MONITORING_URL,
    PASSWORD_AUTH_ENABLED: false,
}

```
Update `nginx.conf` `add_header` values linking to your setups components.
For example:
```
server {
    server_name localhost;
    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/cert.crt;
    ssl_certificate_key /etc/ssl/certs/key.key;

    server_tokens off;
    add_header Content-Security-Policy "upgrade-insecure-requests; default-src 'self'; font-src 'self' data:; img-src 'self' data:; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://PLACEHOLDER RUUTER_URL https://PLACEHOLDER TIM_URL https://PLACEHOLDER CUSTOMER_SERVICE_URL https://PLACEHOLDER PRIV-RUUTER_URL;";


    location / {
      root /usr/share/nginx/html/customer-service;
      try_files $uri /index.html;
    }

    location /status {
      access_log off;
      default_type text/plain;
      add_header Content-Type text/plain;
      return 200 "alive";
    }
}

server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_uri;
}
```

### Running the container

In order to create container from image bring it up like so:
```
docker run \
    -p 3001:443 \
    -v ./nginx.conf:/etc/nginx/conf.d/default.conf \
    -v ./env-config.js:/usr/share/nginx/html/customer-service/env-config.js \
    -v ./cert.crt:/etc/ssl/certs/cert.crt \
    -v ./key.key:/etc/ssl/certs/key.key \
    PLACEHOLDER:IMAGE_NAME 
```

## TIM
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Generate `jwtkeystore.jks` and mount it into the container as `/usr/local/tomcat/jwtkeystore.jks`. The password inserted at `jwtkeystore.jks` creation is used as environmental variable in the container.

### Certificates generation

**Note!** Both keystore password and alias password should be the same.

#### Certificate for JWT signature
```
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore "jwtkeystore.jks" -validity 3650
```
relevant configuration properties:

```
jwt-integration.signature.key-store=classpath:jwtkeystore.jks
jwt-integration.signature.key-store-password=PLACEHOLDER JWT_PASSWORD
jwt-integration.signature.keyStoreType=JKS
jwt-integration.signature.keyAlias=jwtsign
```

#### Regenerating Certificates

To generate a new key pair with certificate:
1. backup the original keystore file.
2. run certificate generation `keytool` command from previous step(s)
3. update configuration with new keystore file and password

#### Changing Keystore password

To change keystore password,
1. run the following command
```
keytool -keystore <keystore file name> -storepasswd
# (old and new password asked)
```
2. update configuration with new password

### Running the container
In order to create container from image bring it up like so:
```
docker run  \
    -p 8085:8443 \
    -e security.allowlist.jwt=PLACEHOLDER ALL_IP_ADDRESSES_WHERE_TRAFFIC_IS_ALLOWED,PLACEHOLDER CONTAINER_NAMES_IF_IN_THE_SAME_NETWORK \
    -e spring.datasource.url=jdbc:postgresql://PLACEHOLDER TIM_DB_ADRESS/tim \
    -e spring.datasource.username=tim \
    -e spring.datasource.password=PLACEHOLDER PASSWORD_FOR_TIM_DATABASE \
    -e security.oauth2.client.client-id=PLACEHOLDER TARA_CLIENT-ID \
    -e security.oauth2.client.client-secret=PLACEHOLDER TARA_CLIENT-SECRET \
    -e security.oauth2.client.registered-redirect-uri=https://PLACEHOLDER TIM_URL/authenticate \
    -e security.oauth2.client.user-authorization-uri=https://tara.ria.ee/oidc/authorize \
    -e security.oauth2.client.access-token-uri=https://tara.ria.ee/oidc/token \
    -e security.oauth2.resource.jwk.key-set-uri=https://tara.ria.ee/oidc/jwks \
    -e auth.success.redirect.whitelist=https://PLACEHOLDER CUSTOMER_SERVICE_URL/auth/callback,https://PLACEHOLDER WIDGET_URL,https://PLACEHOLDER WIDGET_URL/auth/callback,https://PLACEHOLDER CUSTOMER_SERVICE_URL \
    -e frontpage.redirect.url=https://PLACEHOLDER CUSTOMER_SERVICE_URL
    -e "headers.contentSecurityPolicy=upgrade-insecure-requests; default-src 'self' 'unsafe-inline' 'unsafe-eval' https://PLACEHOLDER TIM_URL https://PLACEHOLDER CUSTOMER_SERVICE_URL https://PLACEHOLDER RUUTER_URL https://PLACEHOLDER PRIV-RUUTER_URL byk-tim byk-public-ruuter byk-private-ruuter byk-customer-service; object-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://PLACEHOLDER WIDGET_URL https://PLACEHOLDER CUSTOMER_SERVICE_URL https://PLACEHOLDER TIM_URL; connect-src 'self' https://PLACEHOLDER WIDGET_URL https://PLACEHOLDER TIM_URL https://PLACEHOLDER CUSTOMER_SERVICE_URL https://PLACEHOLDER RUUTER_URL https://PLACEHOLDER PRIV-RUUTER_URL; frame-src 'self'; media-src 'none'" \
    -e legacy-portal-integration.legacyUrl=arendus.eesti.ee \
    -e legacy-portal-integration.legacyPortalRefererMarker=https://arendus.eesti.ee/portaal \
    -e cors.allowedOrigins=https://PLACEHOLDER WIDGET_URL,https://PLACEHOLDER CUSTOMER_SERVICE_URL,https://PLACEHOLDER RUUTER_URL,https://PLACEHOLDER PRIV-RUUTER_URL,https://PLACEHOLDER ANY_SUBDOMAIN_WHICH_IS_USING_THE_WIDGET \
    -e jwt-integration.signature.issuer=test.buerokratt.ee \
    -e jwt-integration.signature.key-store-password=PLACEHOLDER JWTKEYSTORE_PASSWORD \
    -e jwt-integration.signature.key-store=file:/usr/local/tomcat/jwtkeystore.jks \
    -e spring.profiles.active=dev \
    -e legacy-portal-integration.sessionCookieDomain=PLACEHOLDER YOUR_DOMAIN \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./jwtkeystore.jks:/usr/local/tomcat/jwtkeystore.jks \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/key.key \
    PLACEHOLDER:IMAGE_NAME
```

## RESQL
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 8082:8443 \
    -e SPRING_APPLICATION_JSON: '{"sqlms":{"saved-queries-dir":"./templates/","datasources":[{"name":"byk","jdbcUrl":"jdbc:postgresql://PLACEHOLDER USER_DB_ADDRESS:5433/byk?sslmode=require","username":"byk","password":"PLACEHOLDER USERS_DB_PASSWORD","driverClassName":"org.postgresql.Driver"}]}}' \
    -e logging.level.org.springframework.boot=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/key.key \
    PLACEHOLDER:IMAGE_NAME
```

## Monitoring module
Mount certificates into container as `/etc/tls/tls.crt` and `/etc/tls/tls.key`

Update `env-config.js` url-s linking to your setups components.
For example:
```
window._env_ = {
    RUUTER_API_URL: 'https://PLACEHOLDER PRIV-RUUTER_URL',
};

```

Update `nginx.conf` `add_header` values linking to your setups components.
For example:
```
server {
    server_name localhost;
    listen 8443 ssl;
    ssl_certificate /etc/tls/tls.crt;
    ssl_certificate_key /etc/tls/tls.key;

    server_tokens off;
    add_header Content-Security-Policy "upgrade-insecure-requests; default-src 'self'; font-src 'self' data:; img-src 'self' data:; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' PLACEHOLDER PRIV-RUUTER_URL PLACEHOLDER TIM_URL PLACEHOLDER CUSTOMER_SERVICE_URL";

    location / {
      root /usr/share/nginx/html/monitoring;
      try_files $uri /index.html;
    }

    location /status {
      access_log off;
      default_type text/plain;
      add_header Content-Type text/plain;
      return 200 "alive";
    }
}

server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_uri;
}
```

**NB** Private-Ruuter needs to have monitoring url in allowedOrigins list.

### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 81:80 \
    -p 8444:8443 \
    -v ./monitor/nginx.conf:/etc/nginx/conf.d/default.conf \
    -v ./monitor/env-config.js:/usr/share/nginx/html/monitoring/env-config.js \
    -v ./monitor/cert.crt:/etc/tls/tls.crt \
    -v ./monitor/key.key:/etc/tls/tls.key \
    PLACEHOLDER:IMAGE_NAME
```

## License

[MIT](../LICENSE)

## Contributing/Credits

Give thanks and credits for contributors

## How to Contribute

Describe how to contribute
