### About  
##### - This is a workfile of "Guide" for Buerokratt tech team
##### - Workflow is set by dates. Any additions should have name of the contributor
##### - After the final additions, document will be revised and written into a "how to guide"

#### 29.09.22
##### Varmo
Installing the TIM separetaly. It is important, that the databases are installed beforehand, as the TIM relies on tim-postrgesql.

#### tim-postresql.yml
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

The line 18 (has been commented out ATM)

```
command: ["postgres", "-c", "ssl=on", "-c", "ssl_cert_file=/etc/tls/tls.crt", "-c", "ssl_key_file=/etc/tls/tls.key"]
```

This line creats a SSL tunnel between TIM and its database, however, it also creates an error, where logs ell, that the TLS.crt and TLS.key should be owned by a root or admin.
###### Solution - currently working on it
