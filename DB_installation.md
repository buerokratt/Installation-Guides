## About
##### Database installation for Buerokratt

##### Manual install of `users-db` database (Debian based)

Enter the VM designated for databases.
Install Postgres
```
apt-get -y update && apt-get -y install postgresql-client
```
Enter to postgres as superuser
```
su - postgres
```
Create user `byk`
```
create user byk with encrypted password 'PASSWORD';
```
Check if the user `byk` has been created
```
\du+
```
Exit
```
\q
```
Enter to postgres as `byk`
```
PGPASSWORD=BYK psql -U byk -h DB_HOST -p 5432
```
Create database
```
createdb -O byk -e -U byk byk
```
Exit

###### Seed the created database
```
docker run --network=bykstack riaee/byk-users-db:liquibase20220615 bash
```
```
liquibase --url=jdbc:postgresql://DB_HOST:5433/byk?user=byk --password=PASSWORD --changelog-file=/master.yml update"
```
###### Add the configuration
Enter to postgres
```
PGPASSWORD=BYK psql -U byk -h DB_HOST -p 5432
```
Insert configuration
```
insert into configuration(key, value) values ('bot_institution_id', 'bot_name');
```
```
CREATE EXTENSION hstore;
```
You are done. Exit the postgres envorment


##### Users database and TIM-postgresl docker-compose.yml

```
version: '3.9'
services:

  tim-postgresql:
    container_name: tim-postgresql
    image: postgres:14.1
   #command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
    environment:
      - POSTGRES_USER=tim
   user `by`   - POSTGRES_PASSWORD=123
      - POSTGRES_DB=tim
      - POSTGRES_HOST_AUTH_METHOD=trust
    volumes:
      - ./tim-db/cert.crt:/etc/tls/tls.crt
      - ./tim-db/key.key:/etc/tls/tls.key
      - tim-db:/var/lib/postgresql/data
    ports:
      - 5432:5432
    networks:
      - bykstack
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '0.40'
          memory: 150M
        reservations:
          cpus: '0.20'
          memory: 90M

  users-db:
    container_name: users-db
    image: postgres:14.1
   #command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
    environment:
      - POSTGRES_USER=byk
      - POSTGRES_PASSWORD=123
      - POSTGRES_DB=byk
      - POSTGRES_HOST_AUTH_METHOD=trust
    volumes:
      - ./users-db/cert.crt:/etc/tls/tls.crt
      - ./users-db/key.key:/etc/tls/tls.key
      - users-db:/var/lib/postgresql/data
    ports:
      - 5433:5432
    networks:
      - bykstack
    restart: always
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"
    deploy:
      resources:
        limits:
          cpus: '0.40'
          memory: 150M
        reservations:
          cpus: '0.20'
          memory: 80M

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

## Note
#### Known issues
- if you get `404` error in browser while redirecting to `TARA` check the TIM logs `docker logs <TIM container_ID> -f`
Thus far the errors are related to 1) JWT generation error; 2) connection error bwtween TIM and TIM postgresql; 3) wrong info on the lines where TARA info goes
- Remedy: 1) Follow the JWT generation as it is; 2) make sure that ports 5432 and 5433 are allowed 3) make sure you enter correct information

