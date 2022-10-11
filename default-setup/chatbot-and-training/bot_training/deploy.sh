#!/bin/bash

# Replace $USER$ with user folder, where training files are located in
# Replace $SSH-KEY$ with ssh keyname for bot system
# Replace $BOT-USER$ with username of user on bot system
# Replace $BOT-SYSTEM$ with hostname of bot system
# Replace $BOT-CONTAINER-NAME$ with name of the bots container on bot system

BOT_SYSTEM='BOT_ADDRESS'
SSH_KEY='SSH_KEY_PATH'

mkdir -p models/latest-model
cp chatbot-train/models/* models/latest-model/
cp -r chatbot-train/results models/latest-model/
mv models/latest-model models/model-`date +%Y%m%d%H%M%S`
scp -i $SSH_KEY chatbot-train/models/`ls chatbot-train/models/` $BOT_SYSTEM:/opt/bot/loba/models/
ssh $BOT_SYSTEM -i $SSH_KEY  'docker restart byk-bot'
