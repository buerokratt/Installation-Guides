### About  
##### - This is a workfile of "Guide" for Buerokratt tech team
##### - Workflow is set by dates. Any additions should have name of the contributor
##### - After the final additions, document will be revised and written into a "how to guide"

### Directory by name
- [Rainer](#rainer)
- [Varmo](#varmo)
- [Georg](#georg)

### Directory by dates
- [29.09.22](#29-09-22)

#### 21.10
##### Database creation, seeding and adding test-user
Give `cert.crt` and `key.key` files rights. Do it under both `users-db` and `tim-db` folder
```
sudo chown 999:999 key.key
```
```
sudo chmod 0600 key.key
```
```
sudo chown 999:999 cert.crt
```
```
sudo chmod 0600 cert.crt
```

##### Run the databases docker-compose.yml

```
version: '3.9'
services:

  users-db:
    container_name: users-db
    image: postgres:14.1
    command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
    environment:
      - POSTGRES_USER=byk
      - POSTGRES_PASSWORD=01234
      - POSTGRES_DB=byk
    volumes:
      - ./users-db/cert.crt:/etc/tls/tls.crt
      - ./users-db/key.key:/etc/tls/tls.key
      - users-db:/var/lib/postgresql/data
    ports:
      - 5433:5432
    networks:
      - bykstack

  tim-postgresql:
    container_name: tim-postgresql
    image: postgres:14.1
    command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
    environment:
      - POSTGRES_USER=tim
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=tim
    volumes:
      - ./tim-db/cert.crt:/etc/tls/tls.crt
      - ./tim-db/key.key:/etc/tls/tls.key
      - tim-db:/var/lib/postgresql/data
    ports:
      - 5432:5432
    networks:
      - bykstack


volumes:
  users-db:
    driver: local
  tim-db:
    driver: local


networks:
  bykstack:
    name: bykstack
    driver: bridge
```

#### Creating the users database manualy and seeding it

Go into container that is runnoing postgresql users database
```
docker exec -it USERS-DB-CONTAINER bash
```

Insde the container run the commands as follows

```
createdb -O byk -e -U byk byk
```
##### This command is optional. It allows to check and enter into created `byk` database. To exit the database enviorment, use `\q'command
```
psql -h ADDRESS_WHERE_PSQL_IS -p 5433 -U byk
```
```
exit
```
Run the liquibase enviorment to seed your `byk` database
```
docker run -it --network=bykstack riaee/byk-users-db:liquibase20220615 bash
```
Run the `liquibase` command to seed your `byk` database
```
liquibase --url=jdbc:postgresql://USERS-DB-ADDRESS:5432/byk?user=byk --password=01234 --changelog-file=/master.yml update
```
```
exit`
```

#### TIM database manual creation

tim-postgresql
createdb -O tim -e  -U tim tim

Go into container that is running postgresql TIM database
```
docker exec -it TIM-CONTAINER bash
```

Insde the container run the commands as follows

```
createdb -O tim -e -U tim tim
```
##### This command is optional. It allows to check and enter into created `tim` database. To exit the database enviorment, use `\q'command
```
psql -h ADDRESS_WHERE_PSQL_IS -p 5432 -U tim
```
```
exit
```















### 29.09.221
##### Varmo
Installing the TIM separetaly. It is important, that the databases are installed beforehand, as the TIM relies on tim-postrgesql.

### Databases install
#### tim-postresql.yml
### Combined this and users-db.yml into databases.yml. 
```
version: '3.9'
services:

  tim-postgresql:
    container_name: tim-postgresql
    image: postgres:14.1
    # command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
    environment:
      - POSTGRES_USER=tim
      - POSTGRES_PASSWORD=BÄROLL
      - POSTGRES_DB=tim
    volumes:
      - ./tim-db/cert.crt:/etc/tls/tls.crt
      - ./tim-db/key.key:/etc/tls/tls.key
      - tim-db:/var/lib/postgresql/data
    ports:
      - 5432:5432
    networks:
      - bykstack

 
volumes:
 # users-db:
 #   driver: local
  tim-db:
    driver: local
networks:
  bykstack:
    name: bykstack
    driver: bridge
    
```
 
#### Blocker

The line that has been commented out:

```
command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
```

This line creats a SSL tunnel between TIM and its database, however, it also creates an error, where logs tell, that the TLS.crt and TLS.key should be owned by a root or admin.
###### Solution - currently working on it

#### TIM standalone instal

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

##### tim.yml
```
version: '3.9'

services:        
  byk-tim:
    container_name: byk-tim
    image: riaee/byk-tim:07
    environment:
      - security.allowlist.jwt=byk-public-ruuter,byk-private-ruuter,byk-dmapper,byk-widget,byk-customer-service,byk-resql
      - spring.datasource.url=jdbc:postgresql://tim-postgresql:5432/tim
      - spring.datasource.username=tim
      - spring.datasource.password=BÄROLL
      - security.oauth2.client.client-id=tara_client_id
      - security.oauth2.client.client-secret=tara_client_secret
      - security.oauth2.client.registered-redirect-uri=https://tim.byk.buerokratt.ee/authenticate
      - security.oauth2.client.user-authorization-uri=https://tara.ria.ee/oidc/authorize
      - security.oauth2.client.access-token-uri=https://tara.ria.ee/oidc/token
      - security.oauth2.resource.jwk.key-set-uri=https://tara.ria.ee/oidc/jwks
      - auth.success.redirect.whitelist=https://admin.byk.buerokratt.ee/auth/callback,https://byk.buerokratt.ee,https://byk.buerokratt.ee/auth/callback,https://admin.byk.buerokratt.ee
      - frontpage.redirect.url=https://admin.byk.buerokratt.ee
      - "headers.contentSecurityPolicy=upgrade-insecure-requests; default-src 'self' 'unsafe-inline' 'unsafe-eval' https://tim.byk.buerokratt.ee https://admin.byk.buerokratt.ee https://ruuter.byk.buerokratt.ee https://priv-ruuter.byk.buerokratt.ee byk-tim byk-public-ruuter byk-private-ruuter byk-customer-service; object-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://byk.buerokratt.ee https://admin.byk.buerokratt.ee https://tim.byk.buerokratt.ee; connect-src 'self' https://byk.buerokratt.ee https://tim.byk.buerokratt.eehttps://admin.byk.buerokratt.ee https://ruuter.byk.buerokratt.ee https://priv-ruuter.byk.buerokratt.ee; frame-src 'self'; media-src 'none'"
      - legacy-portal-integration.legacyUrl=arendus.eesti.ee
      - legacy-portal-integration.legacyPortalRefererMarker=https://arendus.eesti.ee/portaal
      - cors.allowedOrigins=https://byk.buerokratt.ee,https://admin.byk.buerokratt.ee,https://ruuter.byk.buerokratt.ee,https://priv-ruuter.buerokratt.ee
      - jwt-integration.signature.issuer=byk.buerokratt.ee
      - jwt-integration.signature.key-store-password=safe_keystore_password
      - jwt-integration.signature.key-store=file:/usr/local/tomcat/jwtkeystore.jks
      - spring.profiles.active=dev
      - legacy-portal-integration.sessionCookieDomain=buerokratt.ee
      - logging.level.root=INFO
    ports:
      - 8085:8443
    volumes:
      - ./server.xml:/usr/local/tomcat/conf/server.xml:ro
      - ./jwtkeystore.jks:/usr/local/tomcat/jwtkeystore.jks:ro
      - ./cert.crt:/usr/local/tomcat/conf/cert.crt:ro
      - ./key.key:/usr/local/tomcat/conf/key.key:ro
    restart: always
    networks:
      - bykstack
        
        
networks:
  bykstack:
    name: bykstack
    driver: bridge
```
#### Liquibase install and configuring

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
