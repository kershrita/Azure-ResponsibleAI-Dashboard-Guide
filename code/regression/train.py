import argparse
import shutil

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import ExtraTreesRegressor


def main(args):
    # Read in data
    print("Reading data")
    all_training_data = pd.read_parquet(args.training_data)
    y_train = all_training_data[args.target_column_name]
    X_train = all_training_data.drop([args.target_column_name], axis = 1)  

    # Transform string data to numeric one-hot vectors
    categorical_columns = X_train.select_dtypes("object").columns
    categorial_encoder = OrdinalEncoder()

    # Create a preprocessor that will preprocess both numeric and categorical data
    preprocessor = ColumnTransformer([
    ('categorical-encoder', categorial_encoder, categorical_columns)
    ])

    reg = make_pipeline(
        preprocessor,
        ExtraTreesRegressor(n_estimators=350, max_depth=16, n_jobs=-1, random_state=42)
    )
    
    # Train model
    print("Training model...")
    model = reg.fit(X_train, y_train)
 
    # Save the model with mlflow
    shutil.rmtree(args.model_output, ignore_errors=True)
    mlflow.sklearn.save_model(sk_model=model, path=args.model_output)


# run script
if __name__ == "__main__":
    # add space in logs
    print("*" * 60)
    print("\n\n")

    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--training_data", type=str, help="Path to training data")
    parser.add_argument("--target_column_name", type=str, help="Name of target column")
    parser.add_argument("--model_output", type=str, help="Path of output model")
    args = parser.parse_args()    

    # run main function
    main(args)

    # add space in logs
    print("*" * 60)
    print("\n\n")