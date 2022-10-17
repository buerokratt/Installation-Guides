#!/bin/bash

DIR=/your/actual/directory

cd $DIR || exit 1
echo 'Started training' >> train.log
rm -rf -v chatbot-train/data >> train.log
rm -rf -v chatbot-train/models >> train.log
rm -f -v chatbot-train/domain.yml >> train.log
cp -r -v  chatbot/data chatbot-train >> train.log
cp -v chatbot/domain.yml chatbot-train >> train.log
cp -v chatbot/config.yml chatbot-train >> train.log
mkdir -v chatbot-train/models >> train.log
docker compose up train-bot
docker compose up test-bot
docker compose down
