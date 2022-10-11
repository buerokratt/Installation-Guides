## About
#### Here is described how to deply bot training

- Add Bykstack machines/users public ssh key into Training-Bot machines/users `authorized_keys`. The customer-service component of Bykstack will need access Training-Bot data.

- Create `chatbot` and `chatbot-train` directories to the Bykstack users home directory. Add the same files to both directories as Bot machines `bot_data` [directory](../bot/readme.md#installing).

- Create empty files named `blacklist` in `chatbot/data` and in `chatbot-train/data`.

- Add deploy and train scripts and make them executable.


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
