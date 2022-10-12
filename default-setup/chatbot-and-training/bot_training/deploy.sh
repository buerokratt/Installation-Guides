#!/bin/bash

# Replace $DIR with user folder, where training files are located in
# Replace $SSH_KEY with ssh keyname for bot system
# Replace $BOT_USER with username of user on bot system
# Replace $BOT_HOST with hostname of bot system
# Replace $BOT_CONTAINER_NAME with name of the bots container on bot system

DIR=/your/actual/directory
BOT_HOST='BOT_HOSTNAME'
BOT_USER='BOT_USER'
SSH_KEY='SSH_KEY_PATH'
BOT_CONTAINER_NAME='byk-bot'
BOT_DATA_DIR='/opt/bot/loba'

cd $DIR || exit 1
mkdir -p models/latest-model
cp chatbot-train/models/* models/latest-model/
cp -r chatbot-train/results models/latest-model/
mv models/latest-model models/model-$(date +%Y%m%d%H%M%S)
scp -i $SSH_KEY chatbot-train/models/* $BOT_USER@$BOT_HOST:$BOT_DATA_DIR/models/
ssh $BOT_HOST -i $SSH_KEY -l $BOT_USER "docker restart $BOT_CONTAINER_NAME"
