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
