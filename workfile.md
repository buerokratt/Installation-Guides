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
##### This command is optional. It allows to check and enter into created `byk` database. 
Use these commands to check youd database:
`\l` `\dt` `\db`  
To exit the database enviorment, use `\q` command
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
liquibase --url=jdbc:postgresql://USERS-DB-ADDRESS:5433/byk?user=byk --password=01234 --changelog-file=/master.yml update
```
```
exit`
```

#### TIM database manual creation


Go into container that is running postgresql TIM database
```
docker exec -it TIM-CONTAINER bash
```

Insde the container run the commands as follows

```
createdb -O tim -e -U tim tim
```
##### This command is optional. It allows to check and enter into created `tim` database.
Use these commands to check youd database:
`\l` `\dt` `\db`  
To exit the database enviorment, use `\q` command
```
psql -h ADDRESS_WHERE_PSQL_IS -p 5432 -U tim
```
```
exit
```


#### Dmpper conf
server.xml -> changed so it would not get error on tls certification

```
dmapper server.xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<Server port="8005" shutdown="SHUTDOWN">
    <Listener className="org.apache.catalina.startup.VersionLoggerListener"/>
    <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on"/>
    <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener"/>
    <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener"/>
    <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener"/>

    <GlobalNamingResources>
        <Resource name="UserDatabase" auth="Container"
                  type="org.apache.catalina.UserDatabase"
                  description="User database that can be updated and saved"
                  factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                  pathname="conf/tomcat-users.xml"/>
    </GlobalNamingResources>

    <Service name="Catalina">
        <Connector port="8443"
                   protocol="org.apache.coyote.http11.Http11NioProtocol"
                   clientAuth="false"
                   sslProtocol="TLSv1.2, TLSv1.3"
                   SSLEnabled="true"
                   maxThreads="150"
                   scheme="https"
                   secure="true"
                   SSLCertificateFile="${catalina.base}/conf/tls.crt"
                   SSLCertificateKeyFile="${catalina.base}/conf/tls.key"
        />

        <Engine name="Catalina" defaultHost="localhost">
            <Realm className="org.apache.catalina.realm.LockOutRealm">
                <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
                       resourceName="UserDatabase"/>
            </Realm>

            <Host name="localhost" appBase="webapps"
                  unpackWARs="true" autoDeploy="true">
                <Valve className="org.apache.catalina.valves.ErrorReportValve" showReport="false"
                       showServerInfo="false"/>
                <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
                       prefix="localhost_access_log" suffix=".txt"
                       pattern="%h %l %u %t &quot;%r&quot; %s %b"/>

            </Host>
        </Engine>
    </Service>
</Server>
```

#### TIM conf
#### server.xml
```
<?xml version="1.0" encoding="UTF-8"?>
<!--
  Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<!-- Note:  A "Server" is not itself a "Container", so you may not
     define subcomponents such as "Valves" at this level.
     Documentation at /docs/config/server.html
 -->
<Server port="8005" shutdown="SHUTDOWN">
    <Listener className="org.apache.catalina.startup.VersionLoggerListener"/>
    <!-- Security listener. Documentation at /docs/config/listeners.html
    <Listener className="org.apache.catalina.security.SecurityListener" />
    -->
    <!-- APR library loader. Documentation at /docs/apr.html -->
    <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on"/>
    <!-- Prevent memory leaks due to use of particular java/javax APIs-->
    <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener"/>
    <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener"/>
    <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener"/>

    <!-- Global JNDI resources
         Documentation at /docs/jndi-resources-howto.html
    -->
    <GlobalNamingResources>
        <!-- Editable user database that can also be used by
             UserDatabaseRealm to authenticate users
        -->
        <Resource name="UserDatabase" auth="Container"
                  type="org.apache.catalina.UserDatabase"
                  description="User database that can be updated and saved"
                  factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
                  pathname="conf/tomcat-users.xml"/>
    </GlobalNamingResources>

    <!-- A "Service" is a collection of one or more "Connectors" that share
         a single "Container" Note:  A "Service" is not itself a "Container",
         so you may not define subcomponents such as "Valves" at this level.
         Documentation at /docs/config/service.html
     -->
    <Service name="Catalina">

        <!--The connectors can use a shared executor, you can define one or more named thread pools-->
        <!--
        <Executor name="tomcatThreadPool" namePrefix="catalina-exec-"
            maxThreads="150" minSpareThreads="4"/>
        -->


        <!-- A "Connector" represents an endpoint by which requests are received
             and responses are returned. Documentation at :
             Java HTTP Connector: /docs/config/http.html
             Java AJP  Connector: /docs/config/ajp.html
             APR (HTTP/AJP) Connector: /docs/apr.html
             Define a non-SSL/TLS HTTP/1.1 Connector on port 8080
        -->
        <!--        <Connector port="8080" protocol="HTTP/1.1"-->
        <!--                   connectionTimeout="20000"-->
        <!--                   redirectPort="8443"/>-->
        <!-- A "Connector" using the shared thread pool-->
        <!--
        <Connector executor="tomcatThreadPool"
                   port="8080" protocol="HTTP/1.1"
                   connectionTimeout="20000"
                   redirectPort="8443" />
        -->
        <!-- Define an SSL/TLS HTTP/1.1 Connector on port 8443
             This connector uses the NIO implementation. The default
             SSLImplementation will depend on the presence of the APR/native
             library and the useOpenSSL attribute of the
             AprLifecycleListener.
             Either JSSE or OpenSSL style configuration may be used regardless of
             the SSLImplementation selected. JSSE style configuration is used below.
        -->
        <!--
        <Connector port="8443" protocol="org.apache.coyote.http11.Http11NioProtocol"
                   maxThreads="150" SSLEnabled="true">
            <SSLHostConfig>
                <Certificate certificateKeystoreFile="conf/localhost-rsa.jks"
                             type="RSA" />
            </SSLHostConfig>
        </Connector>
        -->
        <Connector port="8443"
                   protocol="org.apache.coyote.http11.Http11NioProtocol"
                   clientAuth="false"
                   sslProtocol="TLSv1.2, TLSv1.3"
                   SSLEnabled="true"
                   maxThreads="150"
                   scheme="https"
                   secure="true"
                   SSLCertificateFile="${catalina.base}/conf/cert.crt"
                   SSLCertificateKeyFile="${catalina.base}/conf/key.key"
        />
        <!-- Define an SSL/TLS HTTP/1.1 Connector on port 8443 with HTTP/2
             This connector uses the APR/native implementation which always uses
             OpenSSL for TLS.
             Either JSSE or OpenSSL style configuration may be used. OpenSSL style
             configuration is used below.
        -->
        <!--
        <Connector port="8443" protocol="org.apache.coyote.http11.Http11AprProtocol"
                   maxThreads="150" SSLEnabled="true" >
            <UpgradeProtocol className="org.apache.coyote.http2.Http2Protocol" />
            <SSLHostConfig>
                <Certificate certificateKeyFile="conf/localhost-rsa-key.pem"
                             certificateFile="conf/localhost-rsa-cert.pem"
                             certificateChainFile="conf/localhost-rsa-chain.pem"
                             type="RSA" />
            </SSLHostConfig>
        </Connector>
        -->

        <!-- Define an AJP 1.3 Connector on port 8009 -->
        <!--
        <Connector protocol="AJP/1.3"
                   address="::1"
                   port="8009"
                   redirectPort="8443" />
        -->

        <!-- An Engine represents the entry point (within Catalina) that processes
             every request.  The Engine implementation for Tomcat stand alone
             analyzes the HTTP headers included with the request, and passes them
             on to the appropriate Host (virtual host).
             Documentation at /docs/config/engine.html -->

        <!-- You should set jvmRoute to support load-balancing via AJP ie :
        <Engine name="Catalina" defaultHost="localhost" jvmRoute="jvm1">
        -->
        <Engine name="Catalina" defaultHost="localhost">

            <!--For clustering, please take a look at documentation at:
                /docs/cluster-howto.html  (simple how to)
                /docs/config/cluster.html (reference documentation) -->
            <!--
            <Cluster className="org.apache.catalina.ha.tcp.SimpleTcpCluster"/>
            -->

            <!-- Use the LockOutRealm to prevent attempts to guess user passwords
                 via a brute-force attack -->
            <Realm className="org.apache.catalina.realm.LockOutRealm">
                <!-- This Realm uses the UserDatabase configured in the global JNDI
                     resources under the key "UserDatabase".  Any edits
                     that are performed against this UserDatabase are immediately
                     available for use by the Realm.  -->
                <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
                       resourceName="UserDatabase"/>
            </Realm>

            <Host name="localhost" appBase="webapps"
                  unpackWARs="true" autoDeploy="true">
                <Valve className="org.apache.catalina.valves.ErrorReportValve" showReport="false" showServerInfo="false" />

                <!-- SingleSignOn valve, share authentication between web applications
                     Documentation at: /docs/config/valve.html -->
                <!--
                <Valve className="org.apache.catalina.authenticator.SingleSignOn" />
                -->

                <!-- Access log processes all example.
                     Documentation at: /docs/config/valve.html
                     Note: The pattern used is equivalent to using pattern="common" -->
                <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
                       prefix="localhost_access_log" suffix=".txt"
                       pattern="%h %l %u %t &quot;%r&quot; %s %b"/>

            </Host>
        </Engine>
    </Service>
</Server>
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
