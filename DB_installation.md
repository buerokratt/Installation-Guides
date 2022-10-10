## About
##### Database installation for Buerokratt

##### Users database install

Name the file `usersdb.Dockerfile`
```
FROM postgres:14.1 as users-db

ENV POSTGRES_USER byk
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB byk

EXPOSE 5432
```
To instal and run the container, use following command
```
docker build -f usersdb.Dockerfile -t byk-users-db . && docker run --name users-db -p 5432:5432 -d byk-users-db
```


##### Liquibase install

Name the file `liquid.Dockerfile`
```
FROM riaee/byk-users-db:liquibase20220615
RUN liquibase --url=jdbc:postgresql://users-db:5432/byk?user=byk --password=password --changelog-file=/master.yml update

```

To install and run the container, use following command
```
docker build -f liquid.Docerfile .
```

##### Tim-postgresl install

Name the file `tim.Dockerfile`

```
FROM postgres:14.1 as tim-postgres

ENV POSTGRES_USER tim
ENV POSTGRES_PASSWORD safe_tim_password
ENV POSTGRES_DB tim

EXPOSE 5432
```

To install and run the container, usefollowing command

```
docker build -f tim.Dockerfile -t byk-tim-postgresql . && docker run --name tim-postresql -p 5433:5432 -d byk-tim-postgresql
```

### Docker-compose files for database install

##### Tim and users-db install
```
version: '3.9'
services:
  tim-db:
    container_name: tim-db
    build:
      context: tim.Dockerfile
    environment:
      - db_url=tim-postgresql:5432/tim
      - db_user= tim
      - db_user_pswd=123
    ports:
      - 5433:5432
    restart: always
    networks:
      - bykstack

  users-db:
    container_name: users-db
    build:
      context: usersdb.Dockerfile
    environment:
      - POSTGRES_USER=byk
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=byk
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

## Note
- If you have troubles connecting liquibase to users-db, then use IP address instead the containerID
- It is advised to change the password before runningthe Dockerfile's

