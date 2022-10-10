FROM postgres:14.1 as tim-postgres

ENV POSTGRES_USER tim
ENV POSTGRES_PASSWORD safe_tim_password
ENV POSTGRES_DB tim

EXPOSE 5432
