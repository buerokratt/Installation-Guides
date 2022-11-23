#### About
##### Here are listed issues we have witnesed during installation and how to solve them  and also notices to remember

#### Notice - 
While filing the configure.txt file or changint the calues manually, do not end the URL's with `/` as this will cause errors within the system.

##### Issue   
###### Library "TEEMAD" does not load.

- <ins>Description</ins> - After logging in as admin into backoffice GUI, the library "TEEMAD" will not load and you can see the loading circle non-stop. 
 
- <ins>Cause</ins> - It is caused by non-functioning ssh private key. When using `kygen` command you create a key in OPENSH format, that java does not undersand.  
Looking at `private-ruuter` logs, you should see following example lines:    
```
Caused by: com.jcraft.jsch.JSchException: invalid privatekey: [B@67ca1612
```  
        
and  
     
``` 
Unable to call function getBlacklistedIntents  java.lang.reflect.InvocationTargetException: null 
```  
            
This is caused by your RSA </ins>SSH key wrong format. When using `keygen` the defalt format is OPENSSH but it should be RSA  
        
- <ins>Solution</ins> - After you have created your SSH private key, use the command   
 ```
 ssh-keygen -p -f /home/ubuntu/.ssh/id_rsa -m pem 
 ```  
 This will change your key into RSA format.  
 In the `private.urls.docker.json` and `public.urls.docker.json` files, make sure the info is correct, most important, the `training_bot_directory_name`
 ##### For example
 ```
 dmapper_url": "https://byk-dmapper:8443",
    "ruuter_url": "https://localhost:8443",
    "tim_url": "https://byk-tim:8443",
    "resql_url": "https://byk-resql:8443",
    "bot_url": "http://BOT_ADDRESS:5005",
    "training_url": "TRAINING_BOT_ADDRESS",
    "training_user": "ubuntu",
    "training_prv_key":"/home/ubuntu/.ssh/id_rsa",
    "training_bot_directory_name": "/srv/Buerokratt-onboarding/chatbot-installation/Installation-Guides/default-setup/chatbot-and-training/bot_training/chatbot",
```


##### Issue
###### Training the bot results in a "Trained with errors" issue
- <ins>Description</ins> - In backoffice GUI, when you want to train a new bot model, it will result a issue, where it has trained, but with errors  

- <ins>Cause</ins> - Looking in the private-ruuter` logs, you should see the following error/errors
```
2022-11-09T08:49:07.236Z ERROR []  : Unable to call function areLatestTestResultsPositive
```
More info to come

- <ins>Solution</ins> - Solution is to use `/home/username/` folder as the homefolder for trainbot files.


- <ins>Follow-up solution</ins> - To use other folders, rather then /home/, then make sure, that train.sh file has correct paths added and that private.docker.urls.json has correct info. Example below
`train.sh`
```
#!/bin/bash
echo 'Started training' >> train.log
rm -rf -v /opt/bot_training/chatbot-train/data >> train.log
rm -rf -v /opt/bot_training/chatbot-train/models >> train.log
rm -f -v /opt/bot_training/chatbot-train/domain.yml >> train.log
cp -r -v  /opt/bot_training/chatbot/data chatbot-train >> train.log
cp -v /opt/bot_training/chatbot/domain.yml chatbot-train >> train.log
mkdir -v /opt/bot_training/chatbot-train/models >> train.log
docker compose up train-bot
docker compose up test-bot
docker compose down
```
`deploy.sh`
```
#!/bin/bash
# Replace $DIR with user folder, where training files are located in
# Replace $SSH_KEY with ssh keyname for bot system
# Replace $BOT_USER with username of user on bot system
# Replace $BOT_HOST with hostname of bot system
# Replace $BOT_CONTAINER_NAME with name of the bots container on bot system
DIR=/home/ubuntu/lasttest/Installation-Guides/default-setup/chatbot-and-training/bot/loba
BOT_HOST='buerokratt'
BOT_USER='ubuntu'
SSH_KEY='/home/ubuntu/.ssh/authorized_keys'
BOT_CONTAINER_NAME='byk-bot'
BOT_DATA_DIR='/opt/bot/loba'
cd $DIR || exit 1
mkdir -p models/latest-model
cp /opt/bot_training/chatbot-train/models/* models/latest-model/
cp -r /opt/bot_training/chatbot-train/results models/latest-model/
mv /opt/bot_training/models/latest-model models/model-$(date +%Y%m%d%H%M%S)
scp -i $SSH_KEY chatbot-train/models/* $BOT_USER@$BOT_HOST:$BOT_DATA_DIR/models/
ssh $BOT_HOST -i $SSH_KEY -l $BOT_USER "docker restart $BOT_CONTAINER_NAME"
```
`private-ruuter.docker.urls.json`
```
"training_bot_directory_name": "chatbot",
```
##### Issue
###### AUTH FAIL
When your library "Teemad" is not loading and training the bot fails, take a look at your private ruuter logs.
If you spot an error `auth failed` then check if the key type `ssh-rsa` is in `PubkeyAcceptedAlgorithms`


##### Issue
When training module in GUI tells, that "training module is flawed" and cannot be published and private-ruuter logs shw error cause "Cannot find the file"
Make sure that your `bot` is running
