#!/bin/bash

DIR=/your/actual/directory
log_file="$DIR/train.log"

cd $DIR || exit 1
date >> $log_file
echo 'Started training' >> $log_file
rm -rfv chatbot-train/data \
  chatbot-train/models \
  chatbot-train/domain.yml >> $log_file
cp -rv  chatbot/data chatbot/domain.yml chatbot-train/ >> $log_file
mkdir -v chatbot-train/models >> $log_file
docker compose up train-bot >> $log_file
docker compose up test-bot >> $log_file
docker compose down >> $log_file
