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
Do instal and run the container, use following command
```
docker build -t users-db-image . && docker run --name test -p 5432:5432 -d  users-db
```


##### Liquibase install

Name the file `liquid.Dockerfile`
```
FROM riaee/byk-users-db:liquibase20220615
RUN liquibase --url=jdbc:postgresql://localhost:5432/byk?user=byk --password=password --changelog-file=/master.yml update

```

Do install and run the container, use following command
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

Do install and run the container, usefollowing command

```
docker build-f tim.Dockerfile .
```



