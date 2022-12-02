## How to run
To run a docker-compose - 
```
docker-compose up -d
```

#### NOTE
To add analytics and monitoring, add following to the docker-compose.yml
```
  byk-monitor:
    container_name: byk-monitor
    image: riaee/byk:monitoring-20220802
    ports:
      - 81:80
      - 8444:8443
    restart: always
    volumes:
      - ./monitor/cert.crt:/etc/tls/tls.crt
      - ./monitor/key.key:/etc/tls/tls.key
      - ./monitor/nginx.conf:/etc/nginx/conf.d/default.conf
      - ./monitor/env-config.js:/usr/share/nginx/html/monitoring/env-config.js
    networks:
      - bykstack
        
  byk-analytics-be:
    image: opensearchproject/opensearch:1.3.0
    container_name: byk-analytics-be
    environment:
      - DISABLE_INSTALL_DEMO_CONFIG=true
      - discovery.type=single-node
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536 # maximum number of open files for the OpenSearch user, set to at least 65536 on modern systems
        hard: 65536
    volumes:
      - opensearch-data:/usr/share/opensearch/data
      - ./opensearch/jvm.options:/usr/share/opensearch/config/jvm.options
      - ./opensearch/opensearch.yml:/usr/share/opensearch/config/opensearch.yml
      - ./opensearch/config/root-ca.pem:/usr/share/opensearch/config/root-ca.pem
      - ./opensearch/config/admin.pem:/usr/share/opensearch/config/admin.pem
      - ./opensearch/config/admin-key.pem:/usr/share/opensearch/config/admin-key.pem
      - ./opensearch/config/node1.pem:/usr/share/opensearch/config/node1.pem
      - ./opensearch/config/node1-key.pem:/usr/share/opensearch/config/node1-key.pem
      - ./opensearch/securityconfig/config.yml:/usr/share/opensearch/plugins/opensearch-security/securityconfig/config.yml
      - ./opensearch/securityconfig/roles.yml:/usr/share/opensearch/plugins/opensearch-security/securityconfig/roles.yml
      - ./opensearch/securityconfig/roles_mapping.yml:/usr/share/opensearch/plugins/opensearch-security/securityconfig/roles_mapping.yml
    ports:
      - "9200:9200"
      - "9600:9600" # required for Performance Analyzer
    restart: always
    networks:
      - bykstack
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"

  byk-analytics-fe:
    image: opensearchproject/opensearch-dashboards:1.3.0
    container_name: byk-analytics-fe
    volumes:
      - ./opensearch/dashboards.yml:/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml:ro
      - ./opensearch/config/root-ca.pem:/usr/share/opensearch-dashboards/config/root-ca.pem:ro
      - ./opensearch/config/cert.crt:/usr/share/opensearch-dashboards/config/tls.crt:ro
      - ./opensearch/config/key.key:/usr/share/opensearch-dashboards/config/tls.key:ro
      - ./opensearch/assets:/usr/share/opensearch-dashboards/assets:ro
    ports:
      - "5601:5601"
    depends_on:
      - byk-analytics-be
    restart: always
    networks:
      - bykstack
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"

  byk-data-mover:
    image: riaee/byk:chatbot-logstash-20220616
    container_name: byk-data-mover
    volumes:
      - ./logstash/logstash.conf:/usr/share/logstash/config/logstash.conf:ro
      - ./logstash/logstash.yml:/usr/share/logstash/config/logstash.yml:ro
    command: bash -c "logstash -f /usr/share/logstash/config/logstash.conf"
    ports:
      - "8087:8443"
    depends_on:
      - byk-analytics-be
    restart: always
    networks:
      - bykstack
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "3"

volumes:
  opensearch-data:
    driver: local

        
```
