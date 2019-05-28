import datetime as dt
import os
import random

import numpy as np
import pandas as pd


def generate_prediction(start_date: str, end_date: str, n_samples: int, path: str):
    if os.path.isfile(path):
        existing_df = pd.read_csv(path)
    else:
        existing_df = pd.DataFrame()
    results = []
    dates = pd.date_range(start=start_date, end=end_date, freq="S")
    institutions = ["xiaomi", "samsung", "google"]
    classes = ["low", "mid", "high"]
    genders = ["male", "female"]

    for idx in range(n_samples):
        institution = np.random.choice(institutions, size=1).item()
        phone_class = np.random.choice(classes, size=1).item()
        gender = np.random.choice(genders, size=1).item()

        if phone_class == "low":
            value = np.abs(np.random.normal(loc=1000, scale=100., size=1).item())
        elif phone_class == "mid":
            value = np.abs(np.random.normal(loc=2000, scale=200., size=1).item())
        elif phone_class == "high":
            value = np.abs(np.random.normal(loc=3000, scale=300., size=1).item())
        else:
            raise ValueError("Class not recognized")

        if institution == "xiaomi":
            age = np.abs(np.random.normal(loc=20, scale=10, size=1).item())
        elif institution == "google":
            age = np.abs(np.random.normal(loc=40, scale=10, size=1).item())
        elif institution == "samsung":
            age = np.abs(np.random.normal(loc=60, scale=10, size=1).item())
        else:
            raise ValueError("Institution not recognized")

        results.append(
            {
                "prediction_id": random.getrandbits(64),
                "prediction_timestamp": pd.Timestamp(np.random.choice(dates, 1).item()),
                "institutions": institution,
                "class": phone_class,
                "age": age,
                "gender": gender,
                "prediction_value": value,
            }
        )

    new_df = pd.DataFrame(results)[
        ["prediction_id", "prediction_timestamp", "institutions", "class", "age", "gender", "prediction_value"]
    ]
    full_df = pd.concat([existing_df, new_df]).reset_index(drop=True)
    full_df["prediction_timestamp"] = pd.to_datetime(full_df["prediction_timestamp"])
    full_df = full_df.sort_values("prediction_timestamp").reset_index(drop=True)
    full_df.to_csv(path, index=False)
