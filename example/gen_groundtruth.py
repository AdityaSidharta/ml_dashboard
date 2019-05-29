import datetime as dt
import os
import random

import numpy as np
import pandas as pd


def generate_groundtruth(n_samples: int, prediction_path: str, groundtruth_path: str):
    prediction_df = pd.read_csv(prediction_path)
    n_prediction = len(prediction_df)
    assert n_prediction > 0

    if os.path.isfile(groundtruth_path):
        groundtruth_df = pd.read_csv(groundtruth_path)
    else:
        groundtruth_df = pd.DataFrame()
    n_groundtruth = len(groundtruth_df)
    assert (n_groundtruth + n_samples) <= n_prediction
    if n_groundtruth:
        assert (
            prediction_df.loc[: n_groundtruth - 1, "prediction_id"].tolist()
            == groundtruth_df.loc[: n_groundtruth - 1, "prediction_id"].tolist()
        )

    results = []
    for idx, rows in prediction_df.loc[n_groundtruth : (n_groundtruth + n_samples - 1), :].iterrows():
        prediction_id = rows["prediction_id"]
        phone_class = rows["class"]
        prediction_value = rows["prediction_value"]

        if phone_class == "low":
            true_value = np.abs(np.random.normal(loc=1000, scale=200.0, size=1).item())
        elif phone_class == "mid":
            true_value = np.abs(np.random.normal(loc=2000, scale=400.0, size=1).item())
        elif phone_class == "high":
            true_value = np.abs(np.random.normal(loc=3000, scale=600.0, size=1).item())
        else:
            raise ValueError("Class not recognized")

        squared_error = (prediction_value - true_value) ** 2
        absolute_error = np.abs(prediction_value - true_value)
        absolute_percentage_error = np.abs((true_value - prediction_value) / true_value) * 100

        results.append(
            {
                "prediction_id": prediction_id,
                "prediction_value": prediction_value,
                "true_value": true_value,
                "absolute_percentage_error": absolute_percentage_error,
                "squared_error": squared_error,
                "absolute_error": absolute_error,
            }
        )

    new_groundtruth_df = pd.DataFrame(results)[
        [
            "prediction_id",
            "prediction_value",
            "true_value",
            "absolute_percentage_error",
            "squared_error",
            "absolute_error",
        ]
    ]
    full_groundtruth_df = pd.concat([groundtruth_df, new_groundtruth_df]).reset_index(drop=True)
    full_groundtruth_df.to_csv(groundtruth_path, index=False)
