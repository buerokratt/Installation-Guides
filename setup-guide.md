# Bürokratt
Describe what it is and what it is used for
Sort of project overview

## List of dependencies

### External components
* Docker
* docker-compose
### Databases
* PostgreSQL
* Opensearch

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

- [List of dependencies](#list-of-dependencies)
- [Installing](#installing)
- [Using](#using)
- [Forwarding](###Forwarding)
- [License](#license)
- [How to Contribute](#how-to-contribute)

## Installing
The components can be run manually or using tools like [Docker-compose](https://docs.docker.com/compose/). [Here](examples/docker-compose.yml) is example `docker-compose.yml` file. As there is builtin functionality using SSH to transfer data between machines no container orchestration tools can be used in fully functional setup.
As the system can be grouped into 2 parts also 2 machines are needed.
- Bot ~10GB RAM and 10CPU
- Bykstack ~10GB RAM and 7CPU

Additional ressources are needed for SQL database and traffic forwarder/reverse-proxy

**All** components need encrypted traffic between reverse-proxy and its endpoint. Please generate key-cert pairs for every component separately. Except Bot, it doesn't need encrypted local traffic.

### Logging levels

At the moment all components are developed using [Spring](https://spring.io/) framework. Logging level are `ERROR` `WARN` `INFO` `DEBUG` `TRACE`

### CookieDomain

Cookie domain determines from which domain traffic is allowed into Buerokratt system. Top level domain is not recommended due to security concerns. And in the other hand defining domain and sub domains too tightly disables traffic between chat-widgets on different sub domains.

### Databases

#### SQL Databases
Component TIM database gets set up on first run automatically. Users database, used by RESQL, needs some manual steps:
* Creating DB structure
```
docker run -it --network=bykstack PLACEHOLDER USERS_DB_SETUP_IMAGE bash
liquibase --url=jdbc:postgresql://users-db:5432/byk?user=byk --password=PLACEHOLDER USERS_DB_PASSWORD --changelog-file=/master.yml update
```
* Adding first user and configuration

```
docker run -it --network=bykstack ubuntu:latest bash
apt-get -y update && apt-get -y install postgresql-client
psql -d byk -U byk -h users-db -p 5432
insert into user_authority(user_id, authority_name) values ('EE60001019906', '{ROLE_ADMINISTRATOR}'); # Values are here as example
insert into configuration(key, value) values ('bot_institution_id', 'PLACEHOLDER BOT_NAME');
CREATE EXTENSION hstore;
```

#### NO-SQL Databases

##### Opensearch and Dashboards
Official documentation for the Opensearch security plugin configuration [https://opensearch.org/docs/latest/security-plugin/configuration/](https://opensearch.org/docs/latest/security-plugin/configuration/)

##### Topology
The Opensearch and Dashboards containers **must run on the same host machine** as Ruuter containers. Opensearch's cookie (`security_authentication`) is generated via a configuration and Opensearch sets the domain based on where the request is coming from.

##### Resource settings
Add the following row to `/etc/sysctl.conf`, to increase memory available to docker  
`vm.max_map_count=262144`

Add the following rows to `/etc/security/limits.conf`, to unlock JVM memory  
```
# allow user 'opensearch' mlockall
opensearch soft memlock unlimited
opensearch hard memlock unlimited
```

##### TLS
OpenSearch uses TLS in two layers: http and transport (inter-node)
[https://opensearch.org/docs/latest/security-plugin/configuration/generate-certificates/](https://opensearch.org/docs/latest/security-plugin/configuration/generate-certificates/)

Generate your certificates with generate-certificates.sh, `opensearch.yml` is configured to use those certificates. Each node needs their own node certificate and CN on the subject line should be unique for each new node. [https://opensearch.org/docs/latest/security-plugin/configuration/tls#configure-node-certificates](https://opensearch.org/docs/latest/security-plugin/configuration/tls#configure-node-certificates)

**root-ca.pem**: This is the certificate of the root CA that signed all other TLS certificates  
**node1.pem**: This is the certificate that this node uses when communicating with other nodes on the transport layer (inter-node traffic)  
**node1-key.pem**: The private key for the node1.pem node certificate  
**admin.pem**: This is the admin TLS certificate used when making changes to the security configuration. This certificate gives you full access to the cluster  
**admin-key.pem**: The private key for the admin TLS certificate  

##### Authentication
Authentication is determined by config.yml. Described in depth here [https://opensearch.org/docs/latest/security-plugin/configuration/configuration/](https://opensearch.org/docs/latest/security-plugin/configuration/configuration/)  

Dashboards authenticates itself to OpenSearch with basic authentication, described with "basic_internal_auth_domain". Users will be authenticated with TIM generated JWT, described with "jwt_auth_domain". It will be important to customize the signing key parameter with the key retrieved from https://TIM_URL/jwt/verification-key.  

##### Apply all YAML configurations
Start the Opensearch node(s) and run securityadmin.sh inside the docker container. This command uses the default
certificates:  
`./plugins/opensearch-security/tools/securityadmin.sh -cd plugins/opensearch-security/securityconfig/ -icl -nhnv -cacert config/root-ca.pem -cert config/admin.pem -key config/admin-key.pem`

### Private-ruuter
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Update `urls.env.json` url-s linking to your setups components.
For example:
```json
{
  "elastic_url": "http://localhost:9200",
  "dmapper_url": "http://dmapper:8081",
  "ruuter_url": "http://private-ruuter:8443",
  "tim_url": "http://tim:8085",
  "resql_url": "http://resql:8082",
  "bot_url": "http://bot:5005",
  "training_url": "training-machine",
  "training_user": "training-machine-user",
  "training_prv_key": "~/location/of/private/ssh/key",
  "training_bot_directory_name": "location/of/bot/files"
}

```
#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
    -p 8443:8443 \
    -e legacy-portal-integration.sessionCookieDomain=PLACEHOLDER YOUR_DOMAIN \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -e ruuter.cookie.sameSitePolicy=None \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./urls.env.json:/usr/local/tomcat/urls.env.json \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/key.key \
    -v ./location/of/private/ssh/key:/root/.ssh/id_training
```
### Public-ruuter
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Update `urls.env.json` url-s linking to your setups components.
For example:
```json
{
  "elastic_url": "http://PLACEHOLDER NOSQL_DB address/container name:9200",
  "dmapper_url": "http://PLACEHOLDER dmapper_container_name:8081",
  "ruuter_url": "http://PLACEHOLDER public-ruuter_container_name:8443",
  "tim_url": "http://PLACEHOLDER tim_container_name:8085",
  "resql_url": "http://PLACEHOLDER resql_container_name:8082",
  "bot_url": "http://PLACEHOLDER bot_container_name:5005",
}

```
#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
    -p 8443:8443 \
    -e legacy-portal-integration.sessionCookieDomain=PLACEHOLDER YOUR_DOMAIN \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./urls.env.json:/usr/local/tomcat/urls.env.json \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/key.key
```
### DataMapper
Mount certificates into container as `/usr/local/tomcat/conf/tls.crt` and `/usr/local/tomcat/conf/tls.key`

#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
    -p 8081:8443 \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./urls.env.json:/usr/local/tomcat/urls.env.json \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/tls.key
```

### Widget
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
#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
    -p 3000:443 \
    -v ./nginx.conf:/etc/nginx/conf.d/default.conf \
    -v ./index.html:/usr/share/nginx/html/widget/index.html \
    -v ./cert.crt:/etc/tls/tls.crt \
    -v ./key.key:/etc/tls/tls.key
```
### Customer-service
Mount certificates into container as `/etc/ssl/certs/cert.crt` and `/etc/ssl/certs/key.key`

Update `env-config.js` url-s linking to your setups components.
For example:
```json
{
    RUUTER_API_URL: 'https://PLACEHOLDER private-ruuter_container_name:8443',
    TIM_API_URL: 'https://PLACEHOLDER TIM_URL',
    TARA_REDIRECT_URL: 'https://PLACEHOLDER TIM_URL/oauth2/authorization/tara?callback_url=https://PLACEHOLDER ADMIN_URL/auth/callback',
}

```
Update `nginx.conf` `add_header` values linking to your setups components.
For example:
```json
server {
    server_name localhost;
    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/cert.crt;
    ssl_certificate_key /etc/ssl/certs/key.key;

    server_tokens off;
    add_header Content-Security-Policy "upgrade-insecure-requests; default-src 'self'; font-src 'self' data:; img-src 'self' data:; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://PLACEHOLDER RUUTER_URL https://PLACEHOLDER TIM_URL https://PLACEHOLDER ADMIN_URL https://PLACEHOLDER PRIV-RUUTER_URL;";


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
#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
    -p 3001:443 \
    -v ./nginx.conf:/etc/nginx/conf.d/default.conf \
    -v ./env-config.js:/usr/share/nginx/html/customer-service/env-config.js \
    -v ./cert.crt:/etc/ssl/certs/cert.crt \
    -v ./key.key:/etc/ssl/certs/key.key
```

### TIM
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Generate `jwtkeystore.jks` and mount it into the container as `/usr/local/tomcat/jwtkeystore.jks`. The password inserted at `jwtkeystore.jks` creation is used as environmental variable in the container.

#### Certificates generation

**Note!** Both keystore password and alias password should be the same.


##### Certificate for JWT signature
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

##### Regenerating Certificates

To generate a new key pair with certificate:
1. backup the original keystore file.
2. run certificate generation `keytool` command from previous step(s)
3. update configuration with new keystore file and password

##### Changing Keystore password

To change keystore password,
1. run the following command
```
keytool -keystore <keystore file name> -storepasswd
# (old and new password asked)
```
2. update configuration with new password

#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
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
    -e auth.success.redirect.whitelist=https://PLACEHOLDER ADMIN_URL/auth/callback,https://PLACEHOLDER WIDGET_URL,https://PLACEHOLDER WIDGET_URL/auth/callback,https://PLACEHOLDER ADMIN_URL \
    -e frontpage.redirect.url=https://PLACEHOLDER ADMIN_URL
    -e "headers.contentSecurityPolicy=upgrade-insecure-requests; default-src 'self' 'unsafe-inline' 'unsafe-eval' https://PLACEHOLDER TIM_URL https://PLACEHOLDER ADMIN_URL https://PLACEHOLDER RUUTER_URL https://PLACEHOLDER PRIV-RUUTER_URL byk-tim byk-public-ruuter byk-private-ruuter byk-customer-service; object-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://PLACEHOLDER WIDGET_URL https://PLACEHOLDER ADMIN_URL https://PLACEHOLDER TIM_URL; connect-src 'self' https://PLACEHOLDER WIDGET_URL https://PLACEHOLDER TIM_URL https://PLACEHOLDER ADMIN_URL https://PLACEHOLDER RUUTER_URL https://PLACEHOLDER PRIV-RUUTER_URL; frame-src 'self'; media-src 'none'" \
    -e legacy-portal-integration.legacyUrl=arendus.eesti.ee \
    -e legacy-portal-integration.legacyPortalRefererMarker=https://arendus.eesti.ee/portaal \
    -e cors.allowedOrigins=https://PLACEHOLDER WIDGET_URL,https://PLACEHOLDER ADMIN_URL,https://PLACEHOLDER RUUTER_URL,https://PLACEHOLDER PRIV-RUUTER_URL,https://PLACEHOLDER ANY_SUBDOMAIN_WHICH_IS_USING_THE_WIDGET \
    -e jwt-integration.signature.issuer=test.buerokratt.ee \
    -e jwt-integration.signature.key-store-password=PLACEHOLDER JWTKEYSTORE_PASSWORD \
    -e jwt-integration.signature.key-store=file:/usr/local/tomcat/jwtkeystore.jks \
    -e spring.profiles.active=dev \
    -e legacy-portal-integration.sessionCookieDomain=PLACEHOLDER YOUR_DOMAIN \
    -e logging.level.root=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./jwtkeystore.jks:/usr/local/tomcat/jwtkeystore.jks \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/key.key

```

### RESQL
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

#### Running the container
In order to create container from image bring it up like so:
```
docker run PLACEHOLDER:IMAGE_NAME \
    -p 8082:8443 \
    -e SPRING_APPLICATION_JSON: '{"sqlms":{"saved-queries-dir":"./templates/","datasources":[{"name":"byk","jdbcUrl":"jdbc:postgresql://PLACEHOLDER USER_DB_ADDRESS:5433/byk?sslmode=require","username":"byk","password":"PLACEHOLDER USERS_DB_PASSWORD","driverClassName":"org.postgresql.Driver"}]}}' \
    -e logging.level.org.springframework.boot=PLACEHOLDER DESIRED_LOGGING_LEVEL \
    -v ./server.xml:/usr/local/tomcat/conf/server.xml \
    -v ./cert.crt:/usr/local/tomcat/conf/cert.crt \
    -v ./key.key:/usr/local/tomcat/conf/key.key
```

### Logstash
In order to add feedback rating dashboard, there is feedback_rating_dashboard.ndjson file in logstash folder.
To import this file open opensearch dashboards in browser, from left side menu navigate to Stack Management -> Saved Objects
and there is Import button where you can add this file.

Logstash configuration (`logstash.conf`)
```json
input {
  jdbc {
     jdbc_driver_library => "/usr/share/logstash/postgresql-42.3.5.jar"
     jdbc_driver_class => "org.postgresql.Driver"
     jdbc_connection_string => "jdbc:postgresql://database_container_name:5432/byk"
     jdbc_user => "byk"
     jdbc_password => "123"
     type => "chat"
     schedule => "*/5 * * * *"
     statement => "SELECT feedback_rating::INT, * FROM public.chat WHERE created > current_timestamp - interval '5 minutes'"
    }
  jdbc {
     jdbc_driver_library => "/usr/share/logstash/postgresql-42.3.5.jar"
     jdbc_driver_class => "org.postgresql.Driver"
     jdbc_connection_string => "jdbc:postgresql://database_container_name:5432/byk"
     jdbc_user => "byk"
     jdbc_password => "123"
     type => "message"
     schedule => "*/5 * * * *"
     statement => "SELECT * FROM public.message WHERE created > current_timestamp - interval '5 minutes'"
    }
}
output {
  if [type] == "chat" {
      opensearch {
        hosts => "https://opensearch_container_name:9200"
        index => "logstash-logs-chats-%{+YYYY.MM.dd.HH.mm.ss}"
        document_id => index
        doc_as_upsert => true
        auth_type => {
          type => "basic"
          user => "admin"
          password => "admin"
        }
        action => "create"
        ecs_compatibility => disabled
        ssl => true
        ssl_certificate_verification => false
     }
 }
 if [type] == "message" {
    opensearch {
        hosts => "https://opensearch_container_name:9200"
        index => "logstash-logs-message-%{+YYYY.MM.dd.HH.mm.ss}"
        document_id => index
        doc_as_upsert => true
        auth_type => {
          type => "basic"
          user => "admin"
          password => "admin"
        }
        action => "create"
        ecs_compatibility => disabled
        ssl => true
        ssl_certificate_verification => false
     }
 }
}
```

### Setup to enable bot training
Currently the bot training data and ruuter component cannot coexist on the same system and need to be placed on separate systems to enable proper use. 
Necessary steps to ensure training functionalities work properly:
 * Since training data and actions are shared/executed over ssh, users need to be created on both ruuter and training systems (already existing users can be used aswell)
   * set `training_user` value in ruuter urls.env.json as the training system user  
   * generate ssh key for ruuter system and add public key to authorized_keys of training system user folder
   * generate ssh key for training system and add public key to authorized_keys of ruuter system user folder
 * copy necessary bot files to training system (it is recommended to copy the files straight to the training users home directory to mitigate permission errors)
   * necessary files can be found here: https://koodivaramu.eesti.ee/buerokratt/plug-and-play
   * set `training_bot_directory_name` value in ruuter urls.env.json as the directory path `chatbot` folder was copied to - path is referenced from the training user home directory

# Using
Describe how to use running software

###Forwarding

#### Intro
Front-end forwarding functionality can be enabled from customer-service, by changing the env variable
`INSTITUTION_FORWARDING_ENABLED` to either true or false.
for live environment, it is configured in customer-service env file, located in "public/env-config.js"
```js
window._env_ = {
...
INSTITUTION_FORWARDING_ENABLED: true
};

```

#### forwarding setup
Liquibase creates a empty table called 'establishment' which stores all the possible destinations to where a users chat can be forwaded.
New destinations must be added manually, with the fields `name`, `url` and `base_id` filled. base_id is the unique indentifier for each entry.
```sql
INSERT INTO establishment (name, url, base_id )
VALUES ('ruuter-dev-1', 'byk-ruuter-01.PLACEHOLDER', 'base-id-1');
```

#### write only
The table is designed as write only, so existing fields are changed by adding a new row with the same `base_id` and changing the rest of the fields as neccesary.

# License

[MIT](./LICENSE)

# Contributing/Credits

Give thanks and credits for contributors

# How to Contribute
