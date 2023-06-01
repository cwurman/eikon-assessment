from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExperimentFeatures(Base):
    __tablename__ = "experiment_features"

    user_id = Column(Integer, primary_key=True)
    compound_name = Column(String)
    num_experiments_per_user = Column(Integer)
    average_experiment_runtime = Column(Float)
