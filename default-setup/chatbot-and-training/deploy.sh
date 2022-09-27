#!/bin/bash
BOT_SYSTEM= #IP of bot vm
SSH_KEY= #private ssh key path

mkdir -p models/latest-model
cp chatbot-train/models/* models/latest-model/
cp -r chatbot-train/results models/latest-model/
mv models/latest-model models/model-`date +%Y%m%d%H%M%S`
scp -i $SSH_KEY chatbot-train/models/*.tar.gz $BOT_SYSTEM:/opt/bot/loba/models/
ssh $BOT_SYSTEM -i $SSH_KEY  'docker restart byk-bot'
