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
- ssh server
- PostgreSQL DB system
- [TARA](https://www.ria.ee/en/state-information-system/eid/partners.html#tara) contract
- Reverse proxy

# TIM configuration

### Certificates generation

**Note!** Both keystore password and alias password should be the same.

##### Certificate for JWT signature

Open terminal   
In the folder `tim` run the following command
```
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore "jwtkeystore.jks" -validity 3650
```
*relevant configuration properties:

```
jwt-integration.signature.key-store=classpath:jwtkeystore.jks
jwt-integration.signature.key-store-password=JWT_PASSWORD
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
1. Open terminal and run the following command 
```
keytool -keystore <keystore file name> -storepasswd
```
2. update configuration with new password

### Databases
Before installing TIM, you should deploy databases.
TIM database (tim-postgresql is configures automatically during the first deployment)
Users-Database requires manual configuration.
### Run the [docker-compose.yml](../main/default-setup/backoffice-and-bykstack/sql-db/docker-compose.yml) and then [liquibase.yml](../main/default-setup/backoffice-and-bykstack/sql-db/liquibase.yml)

## Private-ruuter configuration

Modify `private.urls.env.json` url-s linking to your setups components.

Open terminal
Under the `ruuter` folder use command:
```
nano private.urls.env.json
```
Modify the lines `bot_url` `raining_url` `training_user` `training_prv_key`
Save and close the file:
```
CTRL X
```
Type `Y` when it asks to save

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

Modify `public.urls.env.json` url-s linking to your setups components.

Open terminal
Under the `ruuter` folder use command:
```
nano public.urls.env.json
```
Modify the lines `bot_url` `raining_url` `training_user` `training_prv_key`
Save and close the file:
```
CTRL X
```
Type `Y` when it asks to save

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
```
CTRL X
```
Type `Y` when it asks to save

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
```
CTRL X
```
Type `Y` when it asks to save


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

```
{
    RUUTER_API_URL: 'https://PRIVATE_RUUTER_URL',
    TIM_API_URL: 'https://TIM_URL',
    TARA_REDIRECT_URL: 'https://TIM_URL/oauth2/authorization/tara?callback_url=https://CUSTOMER_SERVICE_URL/auth/callback',
    MONITORING_URL: https://MONITORING_URL,
    PASSWORD_AUTH_ENABLED: false,
}

```
Modify `nginx.conf` `add_header` values linking to your setups components.

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

# BOT's installation

The bot consists of 2 containers: bot and action server. They should be in one docker network. Example docker-compose file is [here](./default-setup/chatbot-and-training/docker-compose.yml). 

Add Bot-training machines/users public ssh key into Bot machines/users `authorized_keys`. The Bot-training will transfer trained models and restart bot on demand through ssh.

Directory `bot_data` in the example has specific bot data in it. The directory tree looks like this:
```
├── actions
│   ├── action_ask_custom_fallback_form_affirm_deny.py
│   ├── action_check_confidence.py
│   ├── action_files
│   │   ├── bad_intent_description_mapping.csv
│   │   └── intent_description_mapping.csv
│   ├── action_react_to_affirm_deny_in_custom_fallback_form.py
│   ├── action_react_to_affirm_deny_in_direct_to_customer_support_form.py
│   ├── __init__.py
│   └── utils.py
├── config.yml
├── credentials.yml
├── data
│   ├── nlu
│   │   └── *_nlu.yml
│   ├── rules.yml
│   └── stories.yml
├── domain.yml
├── endpoints.yml
├── models
│   └── 20220704-083649-kind-silo.tar.gz
├── README.md
├── results
│   ├── last_model_20220505
│   │   ├── cross
│   │   │   ├── failed_test_stories.yml
│   │   │   ├── intent_confusion_matrix.png
│   │   │   ├── intent_errors.json
│   │   │   ├── intent_histogram.png
│   │   │   ├── intent_report.json
│   │   │   ├── stories_with_warnings.yml
│   │   │   ├── story_confusion_matrix.png
│   │   │   ├── story_report.json
│   │   │   ├── TEDPolicy_confusion_matrix.png
│   │   │   └── TEDPolicy_report.json
│   │   ├── failed_test_stories.yml
│   │   ├── intent_confusion_matrix.png
│   │   ├── intent_errors.json
│   │   ├── intent_histogram.png
│   │   ├── intent_report.json
│   │   ├── stories_with_warnings.yml
│   │   ├── story_confusion_matrix.png
│   │   ├── story_report.json
│   │   ├── TEDPolicy_confusion_matrix.png
│   │   └── TEDPolicy_report.json
│   └── uus
│       ├── cross
│       │   ├── DIETClassifier_confusion_matrix.png
│       │   ├── DIETClassifier_histogram.png
│       │   ├── DIETClassifier_report.json
│       │   ├── failed_test_stories.yml
│       │   ├── intent_confusion_matrix.png
│       │   ├── intent_errors.json
│       │   ├── intent_histogram.png
│       │   ├── intent_report.json
│       │   ├── stories_with_warnings.yml
│       │   ├── story_confusion_matrix.png
│       │   ├── story_report.json
│       │   ├── TEDPolicy_confusion_matrix.png
│       │   └── TEDPolicy_report.json
│       ├── DIETClassifier_confusion_matrix.png
│       ├── DIETClassifier_histogram.png
│       ├── DIETClassifier_report.json
│       ├── failed_test_stories.yml
│       ├── intent_confusion_matrix.png
│       ├── intent_errors.json
│       ├── intent_histogram.png
│       ├── intent_report.json
│       ├── stories_with_warnings.yml
│       ├── story_confusion_matrix.png
│       ├── story_report.json
│       ├── TEDPolicy_confusion_matrix.png
│       └── TEDPolicy_report.json
├── story_graph.dot
└── tests
    ├── test_custom_fallback_policy.yml
    └── test_loba_stories.yml
```

**NB!** If models directory is empty bot training is needed. Refer to [Bot-training]

### Bot

The bot is relaying on fastText pre-trained word vector. [List](https://github.com/facebookresearch/fastText/blob/master/docs/crawl-vectors.md#models) of fastText models. Download and mount model (binary version) according to bots language into the container.

> In the example Estonian model version 300 is used.

`endponts.yml` should have at least action_endpoint.url defined and pointing to Actions server /webhook endpont.

```
action_endpoint:
  url: http://PLACEHOLDER ACTION_SERVER_URL:5055/webhook
```
> If using example docker-compose.yml then action_endpoint.url = http://bot-action-server:5055/webhook

#### Running the container
In order to create container from image bring it up like so:
```
Either docker.compose.yml here or a link to example file. To be added
```

### Action server

#### Running the container
In order to create container from image bring it up like so:
```
Either docker.compose.yml here or a link to example file. To be added
```

## BOT training

The Training-Bot consists of 2 containers: training bot and testing bot. They should be in one docker network. Example docker-compose file is 

- Add Bykstack machines/users public ssh key into Training-Bot machines/users `authorized_keys`. The customer-service component of Bykstack will need access Training-Bot data.

- Create `chatbot` and `chatbot-train` directories to the Bykstack users home directory. Add the same files to both directories as Bot machines `bot_data` directory

- Create empty files named `blacklist` in `chatbot/data` and in `chatbot-train/data`.

- Add deploy and train scripts (see below) and make them executable.

`deploy.sh`
```
#!/bin/bash

BOT_SYSTEM= #IP of bot vm
SSH_KEY= #private ssh key path

mkdir -p models/latest-model
cp chatbot-train/models/* models/latest-model/
cp -r chatbot-train/results models/latest-model/
mv models/latest-model models/model-`date +%Y%m%d%H%M%S`
scp -i $SSH_KEY chatbot-train/models/*.tar.gz $BOT_SYSTEM:/opt/bot/loba/models/
ssh $BOT_SYSTEM -i $SSH_KEY  'docker restart byk-bot'
```

`train.sh`
```
#!/bin/bash
#choo-choo!!

rm -rf chatbot-train/data
rm -rf chatbot-train/models
rm -f chatbot-train/domain.yml
cp -r chatbot/data chatbot-train
cp chatbot/domain.yml chatbot-train
mkdir chatbot-train/models
docker compose up train-bot
docker compose up test-bot
docker compose down

```
The home directory tree looks somewhat like this:
```
├── chatbot
│   ├── README.md
│   ├── actions
│   ├── config.yml
│   ├── credentials.yml
│   ├── data
│   │   ├── blacklist
│   │   ├── nlu
│   │   ├── rules.yml
│   │   └── stories.yml
│   ├── domain.yml
│   ├── endpoints.yml
│   ├── models
│   ├── results
│   ├── story_graph.dot
│   └── tests
├── chatbot-train
│   ├── README.md
│   ├── actions
│   ├── config.yml
│   ├── credentials.yml
│   ├── data
│   │   ├── blacklist
│   │   ├── nlu
│   │   ├── rules.yml
│   │   └── stories.yml
│   ├── domain.yml
│   ├── endpoints.yml
│   ├── models
│   ├── results
│   ├── story_graph.dot
│   └── tests
├── deploy.sh
├── docker-compose.yml
└── train.sh
```

## License

[MIT](../LICENSE)
