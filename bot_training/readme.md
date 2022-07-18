# Training the bot

Components needed to train the chat bot.

## Table of Contents

- [List of dependencies](#list-of-dependencies)
- [Installing](#installing)
  - [Train-Bot](#train-bot)
  - [Test-Bot](#test-bot)
- [License](#license)
- [How to Contribute](#how-to-contribute)

## List of dependencies

- Docker with compose plugin
- ssh server

## Installing

The Training-Bot consists of 2 containers: training bot and testing bot. They should be in one docker network. Example docker-compose file is [here](./examples/docker-compose.yml).

- Add Bykstack machines/users public ssh key into Training-Bot machines/users `authorized_keys`. The customer-service component of Bykstack will need access Training-Bot data.

- Create `chatbot` and `chatbot-train` directories to the Bykstack users home directory. Add the same files to both directories as Bot machines `bot_data` [directory](../bot/readme.md#installing).

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

### Train-Bot

#### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 5006:5005 \
    -e RASA_MAX_CACHE_SIZE=0 \
    -v ./chatbot-train/:/app \
    PLACEHOLDER:IMAGE_NAME train
```

### Test-Bot

#### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 5006:5005 \
    -e RASA_MAX_CACHE_SIZE=0 \
    -v ./chatbot-train/:/app \
    PLACEHOLDER:IMAGE_NAME test --out results/test
```

## License

[MIT](../LICENSE)

## Contributing/Credits

Give thanks and credits for contributors

## How to Contribute

Describe how to contribute
