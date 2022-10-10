# About
#### This is a configuration guide for Buerokratt install
#### This document is addition to a install guide found [here](../main/README.md)

###### Note
The Bykstack consists of 8 - containers, Bots - 3 containers They should be in one docker network. Example docker-compose file is [here](../main/default-setup/backoffice-and-bykstack/docker-compose.yml).

## Bykstack configuring


## Table of Contents

- [List of dependencies](#list-of-dependencies)
- Config files examples
  - [TIM](#tim-configuration)
  - [Private-ruuter](#Private-ruuter-configuration)
  - [Public-ruuter](#Public-ruuter-configuration)
  - [Chat-widget](#Chat-widget-configuration)
  - [Customer-support](#Customer-support-configuration)
  
- [License](#license)

## List of dependencies for installing bykstack

- Docker and docker-compose plugin
- ssh serve
- PostgreSQL DB system
- [TARA](https://www.ria.ee/en/state-information-system/eid/partners.html#tara) contract
- Reverse proxy

# TIM configuration

### Certificates generation

**Note!** Both keystore password and alias password should be the same.

##### Certificate for JWT signature
# NOTE: Following steps have to be executed inside `TIM` container
Open terminal  
Check your `TIM` container ID
```
docker ps -a
```
Run following command
```
docker exec -it tim-byk bash
```
Inside the container run following command
```
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore "jwtkeystore.jks" -validity 3650
```
### Password you create is necessary for later
#####  Note: 'first and last name' == CN => jwt-integration.signature.issuer


After creating ertificates, run following command
```
docker cp <CONTAINER_ID>:/usr/local/tomcat/jwtkeystore.jks jwtkeystore.jks
```
Exit the container
Make sure, that the jwtkeystore.jks is in the `tim` folder if true, run following command
```
sudo chown <YOUR-USERNAME> jwtkeystore.jks
```

### Databases
Before installing TIM, you should deploy databases.
TIM database (tim-postgresql is configures automatically during the first deployment)
Users-Database requires manual configuration.
### Follow the instructios [here](../main/config_draft.md)

## Private-ruuter configuration

Modify `private.urls.docker.json` url-s linking to your setups components.

Open terminal    
``cd ruuter``
Under the `ruuter` folder use command:
```
nano private.urls.docker.json
```
Modify the lines `bot_url` `raining_url` `training_user` `training_prv_key`
Save and close the file:  
`
CTRL S  
CTRL X
`

`private.urls.docker.json` config file example
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
## Public-ruuter configuration

Modify `public.urls.docker.json` url-s linking to your setups components.

Open terminal  
Under the `ruuter` folder use command:
```
nano public.urls.docker.json
```
Modify the lines `bot_url` `raining_url` `training_user` `training_prv_key`
Save and close the file:  
`
CTRL S  
CTRL X
`


`public.urls.docker.json` config file example
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

## Chat-widget configuration

Update `index.html` url-s linking to your setups components.
Where `RUUTER_API_URL` is URL pointing to the Public-ruuter, `TIM_AUTHENTICATION_URL` is URL pointing to the TIM and the URL of the page wher widget is installed into, and:
* `OFFICE_HOURS`: If this variable is added, widget will be hidden when not in defined work hours. If this variable is not added, the widget will always be displayed
  * `TIMEZONE`: Used for comparing the following variables against a specific timezone.
  * `BEGIN`: Beginning of office hours. If current time is before this hour (24H), the widget will not be displayed
  * `END`: End of office hours. If current time is after this hour (24H), the widget will not be displayed
  * `DAYS`: List of days in numbers, where 1=monday, 2=tuesday, 3=wednesday... If current day is in the list of days, the widget will be displayed according to `BEGIN` and `END` times.

Open terminal  
Under the `widget` folder use command:
```
nano index.html
```
Modify the lines `RUUTER_API_URL` and `TIM_AUTHENTICATION_URL` according to your information
Save and close the file:    
`
CTRL S  
CTRL X
`

`index.html` config example

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
    RUUTER_API_URL: 'https://PUBLIC-RUUTER_URL',
    TIM_AUTHENTICATION_URL: 'https://TIM_URL/oauth2/authorization/tara?callback_url=https://URL_WHERE_TO_WIDGET_IS_INSTALLED',
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

Open terminal  
Under the `widget` folder use command:
```
nano nginx.conf
```
Modify the lines `bot_url` `raining_url` `training_user` `training_prv_key`  
Save and close the file:  
`
CTRL S  
CTRL X
`

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
## Customer-support configuration

Modify `env-config.js` url-s linking to your setups components.

Open terminal    
Under the `customer-support` folder use command:
```
nano env-config.js
```
Modify the lines `RUUTER_API_URL` `TIM_API_URL` `TARA_REDIRECT_URL` `MONITORING_URL` according to your information
Save and close the file:  
`
CTRL S  
CTRL X
`

`env-config.js` example

```
window._env_ = {

    RUUTER_API_URL: 'https://PRIVATE_RUUTER_URL',
    TIM_API_URL: 'https://TIM_URL',
    TARA_REDIRECT_URL: 'https://TIM_URL/oauth2/authorization/tara?callback_url=https://CUSTOMER_SERVICE_URL/auth/callback',
    MONITORING_URL: https://MONITORING_URL,
    PASSWORD_AUTH_ENABLED: false,
}

```
Modify `nginx.conf` `add_header` values linking to your setups components.

Open terminal    
Under the `customer-support` folder use command:
```
nano nginx.conf
```
Modify the lines `https://RUUTER_URL` `https://TIM_URL` `https://CUSTOMER_SERVICE_URL` `https://PRIV-RUUTER_URL` according to your information
Save and close the file:  
`
CTRL S  
CTRL X
`

nginx.conf ecxample
```
server {
    server_name localhost;
    listen 443 ssl;
    ssl_certificate /etc/ssl/certs/cert.crt;
    ssl_certificate_key /etc/ssl/certs/key.key;

    server_tokens off;
    add_header Content-Security-Policy "upgrade-insecure-requests; default-src 'self'; font-src 'self' data:; img-src 'self' data:; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self' https://RUUTER_URL https://TIM_URL https://CUSTOMER_SERVICE_URL https://PRIV-RUUTER_URL;";


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



## License

[MIT](../LICENSE)
