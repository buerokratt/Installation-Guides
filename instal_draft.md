#### About
##### This is a install guide for Buerokratt

######
The Bykstack consists of 8 - containers, Bots - 3 containers They should be in one docker network. Example docker-compose file is [here](../main/default-setup/backoffice-and-bykstack/docker-compose.yml).

## Bykstack install

Stack of components handling chat.

## Table of Contents

- [List of dependencies](#list-of-dependencies)
- [Installing](#installing)
  - [tim](#tim)
- [License](#license)

## List of dependencies

- Docker with compose plugin
- ssh server
- PostgreSQL DB system
- [TARA](https://www.ria.ee/en/state-information-system/eid/partners.html#tara) contract
- Reverse proxy

# TIM
##### Creating certificates
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Generate `jwtkeystore.jks` and mount it into the container as `/usr/local/tomcat/jwtkeystore.jks`. The password inserted at `jwtkeystore.jks` creation is used as environmental variable in the container.

### Certificates generation

**Note!** Both keystore password and alias password should be the same.

##### Certificate for JWT signature
```
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore "jwtkeystore.jks" -validity 3650
```
relevant configuration properties:

```
jwt-integration.signature.key-store=classpath:jwtkeystore.jks
jwt-integration.signature.key-store-password=PLACEHOLDER JWT_PASSWORD
jwt-integration.signature.keyStoreType=JKS
jwt-integration.signature.keyAlias=jwtsign
```

#### Regenerating Certificates

To generate a new key pair with certificate:
1. backup the original keystore file.
2. run certificate generation `keytool` command from previous step(s)
3. update configuration with new keystore file and password

#### Changing Keystore password

To change keystore password,
1. run the following command
```
keytool -keystore <keystore file name> -storepasswd
# (old and new password asked)
```
2. update configuration with new password
##### Step 1 - creating certificates
Mount certificates into container as `/usr/local/tomcat/conf/cert.crt` and `/usr/local/tomcat/conf/key.key`

Generate `jwtkeystore.jks` and mount it into the container as `/usr/local/tomcat/jwtkeystore.jks`. The password inserted at `jwtkeystore.jks` creation is used as environmental variable in the container.

### Certificates generation

**Note!** Both keystore password and alias password should be the same.

##### Certificate for JWT signature
```
keytool -genkeypair -alias jwtsign -keyalg RSA -keysize 2048 -keystore "jwtkeystore.jks" -validity 3650
```
relevant configuration properties:

```
jwt-integration.signature.key-store=classpath:jwtkeystore.jks
jwt-integration.signature.key-store-password=PLACEHOLDER JWT_PASSWORD
jwt-integration.signature.keyStoreType=JKS
jwt-integration.signature.keyAlias=jwtsign
```

#### Regenerating Certificates

To generate a new key pair with certificate:
1. backup the original keystore file.
2. run certificate generation `keytool` command from previous step(s)
3. update configuration with new keystore file and password

#### Changing Keystore password

To change keystore password,
1. run the following command
```
keytool -keystore <keystore file name> -storepasswd
# (old and new password asked)
```
2. update configuration with new password

### Databases
Before installing TIM, you should deploy databases.
TIM database (tim-postgresql is configures automatically during the first deployment)
Users-Database requires manual configuration.

### Run the foolowing yml files in order after you change the passwords

##### databases.yml
```
version: '3.9'
services:
  users-postgresql:
    container_name: users-postgresql
    image: postgres:14.1
    environment:
      - POSTGRES_USER=byk
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=byk
      - POSTGRES_HOST_AUTH_METHOD=trust
    ports:
      - 2345:5432
    restart: always
    networks:
      - bykstack
  tim-postgresql:
    container_name: tim-postgresql
    image: postgres:14.1
    environment:
      - POSTGRES_USER=tim
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=tim
      - POSTGRES_HOST_AUTH_METHOD=trust
    ports:
      - 5432:5432
    restart: always
    networks:
      - bykstack

networks:
  bykstack:
    name: bykstack
```

##### Dockerfile
```
FROM riaee/byk-users-db:liquibase20220615

ENV db_url=postgres:5432/byk
ENV db_user=byk
ENV db_user_pswd=123

COPY liquibase.jar /home/liquibase.jar
CMD ["java","-jar","/home/liquibase.jar", "--spring.datasource.url=jdbc:postgresql://${db_url}", "--spring.datasource.username=${db_user}", "--spring.datasource.password=${db_user_pswd}"]
```

##### liquibase.yml
```
version: '3.9'
services:
  byk-users-liquibase:
    build:
      context: .
    environment:
      - db_url=users-postgresql:5432/byk
      - db_user=byk
      - db_user_pswd=123
    ports:
      - 8000:8000
    restart: always
    networks:
      - bykstack
    

networks:
  bykstack:
    name: bykstack
 ```




## License

[MIT](../LICENSE)
