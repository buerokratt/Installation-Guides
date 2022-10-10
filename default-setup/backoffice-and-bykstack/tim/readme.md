# TIM configuration

### Certificates generation

**Note!** Both keystore password and alias password should be the same.

#### Certificate for JWT signature
##### Run a standalone TIM container for creation of JWT key
Go to folder `tim`  
Run following command
```
docker-compose up -d
```
Check, that container name matches `ti-byk-tim` if not, use the containerID or change the `docker exec` parameters according to container name
```
docker ps -a
```
Run following command
```
docker exec -it tim-byk-tim bash
```
### NOTE: Following steps have to be executed inside `TIM` container

Inside the container run following command
```
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore "jwtkeystore.jks" -validity 3650
```

### Password you create is necessary for later
#####  Note: 'first and last name' == CN => jwt-integration.signature.issuer


After creating ertificates, run following command
```
docker cp <CONTAINER_ID>:/usr/local/tomcat/jwtkeystore.jks jwtkeystore.jks
```
Exit the container
Make sure, that the jwtkeystore.jks is in the `tim` folder if true, run following command
```
sudo chown <YOUR-USERNAME> jwtkeystore.jks
```
Stop the container
```
docker stop tim-byk-tim
```
