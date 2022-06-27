## Monitoring design

#### Purpose of this doc, is to express ideas and descisions behind the design of the Buerokratt monitoring (logs and metrics)

#### Design of monitoring logs and metrics

Monitoring system is built:
* Loki (logs); 
* Prometheus (metrics); 
* Grafana (visualization);
* Promtail (discover; ship);
* MinIO (storage);

#### Containers  
Monitoring will be deployed by using docker-compose  

docker-compose.yml  
``` ersion: "3"

networks:
  loki:

services:
  read:
    image: grafana/loki:2.5.0
    command: "-config.file=/etc/loki/config.yaml -target=read"
    ports:
      - 3101:3100
      - 7946
      - 9095
    volumes:
      - ./loki-config.yaml:/etc/loki/config.yaml
    depends_on:
      - minio
    networks: &loki-dns
      loki:
        aliases:
          - loki

  write:
    image: grafana/loki:2.5.0
    command: "-config.file=/etc/loki/config.yaml -target=write"
    ports:
      - 3102:3100
      - 7946
      - 9095
    volumes:
      - ./loki-config.yaml:/etc/loki/config.yaml
    depends_on:
      - minio
    networks:
      <<: *loki-dns

  promtail:
    image: grafana/promtail:2.5.0
    volumes:
      - ./promtailconfig.yaml:/etc/promtail/config.yaml:ro
      - /var/run/docker.sock:/var/run/docker.sock
    command: -config.file=/etc/promtail/config.yaml
    depends_on:
      - gateway
    networks:
      - loki

  minio:
    image: minio/minio
    entrypoint:
      - sh
      - -euc
      - |
        mkdir -p /data/loki-data && \
        mkdir -p /data/loki-ruler && \
        minio server /data
    environment:
      - MINIO_ACCESS_KEY=loki
      - MINIO_SECRET_KEY=supersecret
      - MINIO_PROMETHEUS_AUTH_TYPE=public
      - MINIO_UPDATE=off
    ports:
      - 9000
    volumes:
      - ./.data/minio:/data
    networks:
      - loki

  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_PATHS_PROVISIONING=/etc/grafana/provisioning
      - GF_AUTH_ANONYMOUS_ENABLED=true
      - GF_AUTH_ANONYMOUS_ORG_ROLE=Admin
    depends_on:
      - gateway
    entrypoint:
      - sh
      - -euc
      - |
        mkdir -p /etc/grafana/provisioning/datasources
        cat <<EOF > /etc/grafana/provisioning/datasources/ds.yaml
        apiVersion: 1
        datasources:
          - name: Loki
            type: loki
            access: proxy
            url: http://gateway:3100
            jsonData:
              httpHeaderName1: "X-Scope-OrgID"
            secureJsonData:
              httpHeaderValue1: "tenant1"
        EOF
        /run.sh
    ports:
      - "3000:3000"
    networks:
      - loki

  gateway:
    image: nginx:latest
    depends_on:
      - read
      - write
    entrypoint:
      - sh
      - -euc
      - |
        cat <<EOF > /etc/nginx/nginx.conf
        user  nginx;
        worker_processes  5;  ## Default: 1
        events {
          worker_connections   1000;
        }
        http {
          resolver 127.0.0.11;
          server {
            listen             3100;
            location = / {
              return 200 'OK';
              auth_basic off;
            }
            location = /api/prom/push {
              proxy_pass       http://write:3100\$$request_uri;
            }
            location = /api/prom/tail {
              proxy_pass       http://read:3100\$$request_uri;
              proxy_set_header Upgrade \$$http_upgrade;
              proxy_set_header Connection "upgrade";
            }
            location ~ /api/prom/.* {
              proxy_pass       http://read:3100\$$request_uri;
            }
            location = /loki/api/v1/push {
              proxy_pass       http://write:3100\$$request_uri;
            }
            location = /loki/api/v1/tail {
              proxy_pass       http://read:3100\$$request_uri;
              proxy_set_header Upgrade \$$http_upgrade;
              proxy_set_header Connection "upgrade";
            }
            location ~ /loki/api/.* {
              proxy_pass       http://read:3100\$$request_uri;
            }
          }
        }
        EOF
        /docker-entrypoint.sh nginx -g "daemon off;"
    ports:
      - "3100:3100"
    networks:
      - loki 
``` 

##### Note  
Gateway in docker-compose.yml is currently for testing purposes, it might be removed depending on if I decide to use gateway as primary activity tunnel (where the traffic goes through)

promtailconfig.yml
```
---
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://gateway:3100/loki/api/v1/push
    tenant_id: tenant1

scrape_configs:
  - job_name: flog_scrape 
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        regex: '/(.*)'
        target_label: 'container'
``` 

##### Note  
Promtail scrape_config line must be modified, so that the pulled logs modification happens in here. (Work in progress)   
Steps to research: does monitoring logs in the scope that has been talked about, is the way to proceed as of now ? Possibe solution/replacement -> Prometheus metrics. This allows me to collect the metrics of the single/cluster instance without need to collect sensitive info from the client.
