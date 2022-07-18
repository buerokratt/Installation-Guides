# Bot

The bot that talks to user.

## Table of Contents

- [List of dependencies](#list-of-dependencies)
- [Installing](#installing)
- [License](#license)
- [How to Contribute](#how-to-contribute)

## List of dependencies

- Docker with compose plugin
- ssh server
## Installing

The bot consists of 2 containers: bot and action server. They should be in one docker network. Example docker-compose file is [here](./examples/docker-compose.yml). 

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
**NB!** If models directory is empty bot training is needed. Refer to [Bot-training](../bot_training/readme.md)
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
docker run \
    -p 5005:5005 \
    -v ./cc.et.300.bin:/app/fasttext_et_model/cc.et.300.bin:ro \
    -v ./bot_data/:/app \
    PLACEHOLDER:IMAGE_NAME
```

### Action server

#### Running the container
In order to create container from image bring it up like so:
```
docker run \
    -p 5055:5055 \
    -v ./bot_data/actions:/app/actions \
    -v ./bot_data/data:/app/data \
    PLACEHOLDER:IMAGE_NAME
```
## License

[MIT](../LICENSE)

## Contributing/Credits

Give thanks and credits for contributors

## How to Contribute

Describe how to contribute
