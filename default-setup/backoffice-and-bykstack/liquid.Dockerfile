FROM riaee/byk-users-db:liquibase20220615
RUN liquibase --url=jdbc:postgresql://users-db:5432/byk?user=byk --password=123 --changelog-file=/master.yml update
