### A directory to store users db certificates

## Seeding DB

```
docker run -it --network=bykstack riaee/byk-users-db:liquibase20220615 bash
liquibase --url=jdbc:postgresql://users-db:5432/byk?user=byk --password=PASSWORD_PLACEHOLDER --changelog-file=/master.yml update

```

## adding first use

```
docker run -it --network=bykstack ubuntu:latest bash
apt-get -y update && apt-get -y install postgresql-client
psql -d byk -U byk -h users-db -p 5432
insert into user_authority(user_id, authority_name) values ('EE60001019906', '{ROLE_ADMINISTRATOR}'); #adds Märy Änn
insert into configuration(key, value) values ('bot_institution_id', 'test');
CREATE EXTENSION hstore;
```

