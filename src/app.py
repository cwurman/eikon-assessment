from flask import Flask

from etl import perform_etl_job

app = Flask(__name__)


@app.route("/trigger_etl/", methods=["GET"])
def trigger_etl():
    """
    For simplicity's sake, just run the ETL process synchronously.
    If this job were more resource intensive, I would execute async and return immediately that the job had started.
    Then, we could execute the ETL process in the backend, either in another thread/process, or potentially using
          another task orchestrator like Celery or Airflow.
    """
    perform_etl_job("data")
    return {"message": "ETL process completed"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
