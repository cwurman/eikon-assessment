import os
from collections import Counter
from contextlib import contextmanager

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_model import ExperimentFeatures


def load_data(data_dir: str):
    """
    Load and return data from a specified data directory.
    :param data_dir:
    :return: a tuple of (users_df, compounds_df, experiments_df)
    """
    with open(f"{data_dir}/users.csv", "r") as fp:
        users_df = pd.read_csv(fp)
    with open(f"{data_dir}/compounds.csv", "r") as fp:
        compounds_df = pd.read_csv(fp)
    with open(f"{data_dir}/user_experiments.csv", "r") as fp:
        experiments_df = pd.read_csv(fp)

    return users_df, compounds_df, experiments_df


def extract_features_from_data(data_dir: str):
    """
    Extract the desired features from a data directory, assuming the data directory has a `user_experiments.csv`.
    :param data_dir: Name of directory containing the `user_experiments.csv`
    :return: A dataframe with:
        - User ID
        - Total number of experiments run by a user
        - Average experiment runtime for a user
        - Most commonly used experimental compound for a user (if ties, return only one)
    """
    users_df, compounds_df, experiments_df = load_data(data_dir=data_dir)

    # total number of experiments run per user
    num_experiments_per_user = (
        experiments_df.user_id.value_counts()
        .rename_axis("user_id")
        .reset_index(name="num_experiments_per_user")
    )

    # average experiment runtime per user
    average_experiment_runtime = (
        experiments_df.groupby("user_id")["experiment_run_time"]
        .mean()
        .reset_index(name="average_experiment_runtime")
    )

    # most common experiment compound per user
    aggregated_experiment_compound_ids = experiments_df.groupby(
        ["user_id"], as_index=False
    ).agg({"experiment_compound_ids": ";".join})
    aggregated_experiment_compound_ids[
        "compound_id"
    ] = aggregated_experiment_compound_ids.experiment_compound_ids.apply(
        lambda L: Counter(L.split(";")).most_common(1)[0][0]
    ).astype(int)

    extracted_features = aggregated_experiment_compound_ids.merge(compounds_df, on="compound_id")[["user_id", "compound_name"]]
    extracted_features.rename(columns={"compound_name": "most_common_compound_name"})
    extracted_features = extracted_features.merge(num_experiments_per_user, on="user_id")
    extracted_features = extracted_features.merge(average_experiment_runtime, on="user_id")

    return extracted_features


@contextmanager
def db_session(engine):
    session = sessionmaker(bind=engine)()

    try:
        yield session
        session.commit()  # Commit the changes upon successful execution
    except:
        session.rollback()  # Rollback the changes in case of an exception
        raise
    finally:
        session.close()  # Close the session


def upload_features_df_to_database(features_df):
    """
    Uploads our dataframe to the database
    :param features_df: The dataframe to insert into our ExperimentFeatures table
    :return: None
    """
    POSTGRES_USER = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_PORT = os.environ["POSTGRES_PORT"]
    POSTGRES_DB = os.environ["POSTGRES_DB"]
    db_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{POSTGRES_PORT}/{POSTGRES_DB}"

    engine = create_engine(db_url)
    with db_session(engine=engine) as session:
        features_rows = [
            ExperimentFeatures(**feature)
            for feature in features_df.to_dict(orient="records")
        ]

        session.add_all(features_rows)


def perform_etl_job(data_dir: str):
    """
    Loads in data from a specified data directory, processes features, and uploads to a database.
    :param data_dir: local directory to find files
    :return: None
    """
    features_df = extract_features_from_data(data_dir=data_dir)
    upload_features_df_to_database(features_df=features_df)
