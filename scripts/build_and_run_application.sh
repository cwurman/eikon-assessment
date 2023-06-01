#!/bin/bash -ex

docker build -t etl-application:latest .

# Run the container with the name "etl-application-container" so we can easily hit the database later!
docker run -p 8080:80 --name etl-application-container etl-application:latest
