## About
### This is a guide to deploy Bot and Bot-training

### BOT's installation

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
