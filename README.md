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

From the root of this repo, execute `./scripts/build_and_run_application.sh` .

This will build and run the docker image locally. The application is ready when you see the Flask dev server output, something like this:
```
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:80
 * Running on http://10.17.205.79:80
Press CTRL+C to quit
 * Serving Flask app 'app'
 * Debug mode: off
```


### Using the application

From the root of this repo, execute `./scripts/use_application.sh` to hit the API that is exposed by the docker container & trigger our ETL job!
It has succeeded if you see an output like this:

```
{"message":"ETL process completed"}
```

### Verify that our ETL job worked

Once our ETL job worked, we can query the database that is also running in our docker container and verify that our info has been loaded into it.
Execute `./scripts/query_database.sh` to do so!

If everything worked as expected, you should see an output that looks like the intended extracted features from our data:
```
 user_id | compound_name | num_experiments_per_user | average_experiment_runtime 
---------+---------------+--------------------------+----------------------------
       1 | Compound B    |                        2 |                     12.500
       3 | Compound B    |                        1 |                     25.000
       5 | Compound B    |                        1 |                     35.000
       7 | Compound B    |                        1 |                     45.000
       9 | Compound B    |                        1 |                     55.000
       2 | Compound A    |                        1 |                     20.000
       4 | Compound A    |                        1 |                     30.000
       6 | Compound A    |                        1 |                     40.000
       8 | Compound A    |                        1 |                     50.000
      10 | Compound A    |                        1 |                     60.000
```
