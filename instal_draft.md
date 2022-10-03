### About
##### This is a install guide for Buerokratt

######
The Bykstack consists of 8 - containers, Bots - 3 containers They should be in one docker network. Example docker-compose file is [here](../main/default-setup/backoffice-and-bykstack/docker-compose.yml).

## Bykstack install

Stack of components handling chat.

## Table of Contents

- [List of dependencies](#list-of-dependencies)
- [Installing](#installing)
  - [TIM](#tim)
  - [Private-ruuter](#Private-ruuter)
  - [Public-ruuter](#Public-ruuter)
  - [Chat-widget](#Chat-widget)
  - [Customer-support](#Customer-support)
  - [RESQL](#RESQL)
- [License](#license)

## List of dependencies

- Docker and docker-compose plugin
- ssh server
- PostgreSQL DB system
- [TARA](https://www.ria.ee/en/state-information-system/eid/partners.html#tara) contract
- Reverse proxy

# TIM
##### Creating certificates
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Generate `jwtkeystore.jks` and mount it into the container as `/usr/local/tomcat/jwtkeystore.jks`. The password inserted at `jwtkeystore.jks` creation is used as environmental variable in the container.

### Certificates generation

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
##### Step 1 - creating certificates
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Generate `jwtkeystore.jks` and mount it into the container as `/usr/local/tomcat/jwtkeystore.jks`. The password inserted at `jwtkeystore.jks` creation is used as environmental variable in the container.

### Certificates generation

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

### Databases
Before installing TIM, you should deploy databases.
TIM database (tim-postgresql is configures automatically during the first deployment)
Users-Database requires manual configuration.

### Run the following yml files in order after you change the passwords

##### databases.yml
```
version: '3.9'
services:
  users-postgresql:
    container_name: users-postgresql
    image: postgres:14.1
    environment:
      - POSTGRES_USER=byk
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=byk
      - POSTGRES_HOST_AUTH_METHOD=trust
    ports:
      - 2345:5432
    restart: always
    networks:
      - bykstack
  tim-postgresql:
    container_name: tim-postgresql
    image: postgres:14.1
    environment:
      - POSTGRES_USER=tim
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=tim
      - POSTGRES_HOST_AUTH_METHOD=trust
    ports:
      - 5432:5432
    restart: always
    networks:
      - bykstack

networks:
  bykstack:
    name: bykstack
```

##### Dockerfile
```
FROM riaee/byk-users-db:liquibase20220615

ENV db_url=postgres:5432/byk
ENV db_user=byk
ENV db_user_pswd=123

COPY liquibase.jar /home/liquibase.jar
CMD ["java","-jar","/home/liquibase.jar", "--spring.datasource.url=jdbc:postgresql://${db_url}", "--spring.datasource.username=${db_user}", "--spring.datasource.password=${db_user_pswd}"]
```

##### liquibase.yml
```
version: '3.9'
services:
  byk-users-liquibase:
    build:
      context: .
    environment:
      - db_url=users-postgresql:5432/byk
      - db_user=byk
      - db_user_pswd=123
    ports:
      - 8000:8000
    restart: always
    networks:
      - bykstack
    

networks:
  bykstack:
    name: bykstack
 ```
 
 ## Private-ruuter
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Update `urls.env.json` url-s linking to your setups components.
For example:
```json
{
  "dmapper_url": "https://byk-dmapper:8443",
  "ruuter_url": "https://localhost:8443",
  "tim_url": "https://byk-tim:8443",
  "resql_url": "https://byk-resql:8443",
  "bot_url": "http://BOT_IP:5005",
  "training_url": "TRAINIG_BOT",
  "training_user": "TRAINING_BOT_USERNAME",
  "training_prv_key": "TRAINIG_BOT_PRIVATE_SSH_KEY_PATH",
  "training_bot_directory_name": "TRAINING_DATA_DIRECTORY",
  "gazetteer_url":"https://inaadress.maaamet.ee/inaadress",
  "publicapi_url": "https://publicapi.envir.ee/v1/combinedWeatherData",
  "ilmmicroservice_url": "https://ilmmicroservice.envir.ee/api/forecasts"
}
```
## Public-ruuter
 ## Private-ruuter
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Update `urls.env.json` url-s linking to your setups components.
For example:
```json
{
  "dmapper_url": "https://byk-dmapper:8443",
  "ruuter_url": "https://localhost:8443",
  "tim_url": "https://byk-tim:8443",
  "resql_url": "https://byk-resql:8443",
  "bot_url": "http://BOT_IP:5005",
  "training_url": "TRAINIG_BOT",
  "training_user": "TRAINING_BOT_USERNAME",
  "training_prv_key": "TRAINIG_BOT_PRIVATE_SSH_KEY_PATH",
  "training_bot_directory_name": "TRAINING_DATA_DIRECTORY",
  "gazetteer_url":"https://inaadress.maaamet.ee/inaadress",
  "publicapi_url": "https://publicapi.envir.ee/v1/combinedWeatherData",
  "ilmmicroservice_url": "https://ilmmicroservice.envir.ee/api/forecasts"
}
```

## Chat-widget

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
    add_header 'Access-Control-Allow-Origin' 'https://FIRST_PAGE_WITH_WIDGET' always;
    add_header 'Access-Control-Allow-Origin' 'https://SECOND_PAGE_WITH_WIDGET' always;

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
## Customer-service

Mount certificates into container as `/etc/ssl/certs/cert.crt` and `/etc/ssl/certs/key.key`

Update `env-config.js` url-s linking to your setups components.
For example:
```
{
    RUUTER_API_URL: 'https://PRIVATE_RUUTER_URL',
    TIM_API_URL: 'https://TIM_URL',
    TARA_REDIRECT_URL: 'https://TIM_URL/oauth2/authorization/tara?callback_url=https://CUSTOMER_SERVICE_URL/auth/callback',
    MONITORING_URL: https://MONITORING_URL,
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

## RESQL
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`



## License

[MIT](../LICENSE)
