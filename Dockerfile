FROM python:3.9-slim

#### Database setup & initialization ####

RUN apt-get update && apt-get install -y postgresql-client postgresql

COPY init_database.sql /work/init_database.sql
WORKDIR /work
# Run an init script on the database to setup the table schema
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
    createdb -O docker experiments_database &&\
    psql experiments_database < init_database.sql
USER root


# Again, for simplicity's sake, just setup a simple postgres server on this same image with auth that we can pass
# to our main application process.
# To make this more robust, we could have the postgres server and the API server running on separate containers, and have
# a secure secrets storage mechanism that is used both by the postgres image and the API server image to access the DB.
ENV POSTGRES_USER docker
ENV POSTGRES_PASSWORD docker
ENV POSTGRES_DB experiments_database
ENV POSTGRES_PORT 5432

#### Application setup ####

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install -r requirements.txt

COPY src/ /app/
COPY data/ /app/data/

EXPOSE 80

CMD service postgresql start && python3 app.py
