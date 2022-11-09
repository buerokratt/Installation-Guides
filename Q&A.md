#### About
##### Here are listed issues we have witnesed during installation and how to solve them  

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

- <ins>Solution</ins> - Solution on how to fix it, is to come



