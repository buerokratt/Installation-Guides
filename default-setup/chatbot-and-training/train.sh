#!/bin/bash
#choo-choo!!

rm -rf chatbot-train/data
rm -rf chatbot-train/models
rm -f chatbot-train/domain.yml
cp -r chatbot/data chatbot-train
cp chatbot/domain.yml chatbot-train
mkdir chatbot-train/models
docker-compose up train-bot
docker-compose up test-bot
docker-compose down
