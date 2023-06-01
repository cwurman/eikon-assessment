#!/bin/bash -ex

export POSTGRES_USER=docker
export POSTGRES_DB=experiments_database
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432

psql_config="-U ${POSTGRES_USER} -d ${POSTGRES_DB} -h ${POSTGRES_HOST}  -p ${POSTGRES_PORT}"
psql_command='SELECT * from experiment_features;'

echo "Querying the database after running our ETL command!"
docker exec -e PGPASSWORD=docker etl-application-container psql $psql_config -c "$psql_command"
