CREATE TABLE experiment_features (
    user_id integer NOT NULL,
    compound_name text NOT NULL,
    num_experiments_per_user integer NOT NULL,
    average_experiment_runtime numeric(7,3) NOT NULL
);
