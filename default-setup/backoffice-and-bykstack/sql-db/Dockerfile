FROM riaee/byk-users-db:liquibase20220615

ENV db_url=postgres:5432/byk
ENV db_user=byk
ENV db_user_pswd=123

COPY liquibase.jar /home/liquibase.jar
CMD ["java","-jar","/home/liquibase.jar", "--spring.datasource.url=jdbc:postgresql://${db_url}", "--spring.datasource.username=${db_user}", "--spring.datasource.password=${db_user_pswd}"]

