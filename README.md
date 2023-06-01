# eikon-assessment

This repository contains the end-to-end runnable code for the Eikon take home assessment!

## Prerequisites

Before running this application locally, you must have the following installed on your machine:
 * docker
 * curl
 * psql

## Local setup & development
To setup the local repo for development, use your env manager of choice to create an environment from the `requirements.txt` file.

For example, using conda:
```
conda create -n eikon-assessment python=3.8 -f requirements.txt
conda activate eikon-assessment
```

## Building and Running

### Building and Running the Container

Execute `./scripts/build_and_run_application.sh` .

This will build and run the docker image locally.


### Using the application

Execute `./scripts/use_application.sh` to hit the API that is exposed by the docker container & trigger our ETL job!

### Verify that our ETL job worked

Once our ETL job worked, we can query the database that is also running in our docker container and verify that our info has been loaded into it.
Execute `./scripts/query_database.sh` to do so!
