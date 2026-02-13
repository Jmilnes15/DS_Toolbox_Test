"""
Data loading utilities for the Clinical Control Tower app.
Loads CSVs and model artifacts. In production, this would read from
Pins on Posit Connect for versioned, governed data access.
"""

import pandas as pd
import numpy as np
import json
import os
import pickle

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")


def load_studies():
    df = pd.read_csv(os.path.join(DATA_DIR, "studies.csv"))
    df["start_date"] = pd.to_datetime(df["start_date"])
    df["planned_end_date"] = pd.to_datetime(df["planned_end_date"])
    return df


def load_sites():
    df = pd.read_csv(os.path.join(DATA_DIR, "sites.csv"))
    df["activation_date"] = pd.to_datetime(df["activation_date"])
    df["last_monitoring_visit"] = pd.to_datetime(df["last_monitoring_visit"])
    return df


def load_enrollment_ts():
    df = pd.read_csv(os.path.join(DATA_DIR, "enrollment_timeseries.csv"))
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_risk_signals():
    df = pd.read_csv(os.path.join(DATA_DIR, "risk_signals.csv"))
    df["detected_date"] = pd.to_datetime(df["detected_date"])
    return df


def load_site_rankings():
    path = os.path.join(DATA_DIR, "site_rankings.csv")
    if os.path.exists(path):
        return pd.read_csv(path)
    return pd.DataFrame()


def load_kpis():
    with open(os.path.join(DATA_DIR, "kpi_summary.json")) as f:
        return json.load(f)


def load_enrollment_model():
    path = os.path.join(MODEL_DIR, "enrollment_forecaster.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


def load_enrollment_model_metrics():
    path = os.path.join(MODEL_DIR, "enrollment_forecaster_metrics.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def load_risk_model():
    path = os.path.join(MODEL_DIR, "risk_classifier.pkl")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    return None


def load_risk_model_metrics():
    path = os.path.join(MODEL_DIR, "risk_classifier_metrics.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {}


def forecast_enrollment(study_id, weeks_ahead=12):
    """Generate enrollment forecast for a study."""
    ts = load_enrollment_ts()
    model = load_enrollment_model()
    study_ts = ts[ts["study_id"] == study_id].sort_values("week")

    if len(study_ts) == 0 or model is None:
        return pd.DataFrame()

    last_row = study_ts.iloc[-1]
    target = last_row["target_enrollment"]
    cumulative = last_row["cumulative_enrolled"]
    last_week = last_row["week"]

    forecasts = []
    for w in range(1, weeks_ahead + 1):
        week = last_week + w
        enrollment_ratio = cumulative / max(1, target)
        gap_ratio = (last_row["planned_cumulative"] - cumulative) / max(1, target)
        week_sin = np.sin(2 * np.pi * week / 52)
        week_cos = np.cos(2 * np.pi * week / 52)

        features = np.array([[week, cumulative, enrollment_ratio, gap_ratio,
                               target, week_sin, week_cos]])
        predicted = max(0, int(model.predict(features)[0]))
        cumulative = min(target, cumulative + predicted)

        forecast_date = last_row["date"] + pd.Timedelta(weeks=w)
        forecasts.append({
            "study_id": study_id,
            "week": week,
            "date": forecast_date,
            "predicted_enrolled": predicted,
            "cumulative_forecast": cumulative,
            "target_enrollment": target,
            "is_forecast": True,
        })

    return pd.DataFrame(forecasts)
