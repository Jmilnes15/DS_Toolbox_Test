"""
Clinical Control Tower - Model Training Pipeline
==================================================
Trains predictive models for:
  1. Enrollment Forecasting (time-series regression)
  2. Site Risk Scoring (classification)
  3. Site Ranking (composite scoring model)

In production, this would run as a scheduled Quarto document on Posit Connect,
with models versioned and stored via Vetiver + Pins.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import cross_val_score
import pickle
import os
import json
from datetime import datetime

MODEL_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def train_enrollment_forecaster():
    """
    Train a model to predict future enrollment rates.
    Features: week number, current cumulative, gap to plan, target.
    Target: next week's enrollment count.
    """
    print("Training enrollment forecasting model...")
    ts = pd.read_csv(os.path.join(DATA_DIR, "enrollment_timeseries.csv"))

    # Feature engineering
    ts["enrollment_ratio"] = ts["cumulative_enrolled"] / ts["target_enrollment"].clip(lower=1)
    ts["gap_ratio"] = ts["enrollment_gap"] / ts["target_enrollment"].clip(lower=1)
    ts["week_sin"] = np.sin(2 * np.pi * ts["week"] / 52)
    ts["week_cos"] = np.cos(2 * np.pi * ts["week"] / 52)

    # Create next-week prediction target
    ts["next_week_enrolled"] = ts.groupby("study_id")["weekly_enrolled"].shift(-1)
    ts = ts.dropna(subset=["next_week_enrolled"])

    features = ["week", "cumulative_enrolled", "enrollment_ratio", "gap_ratio",
                 "target_enrollment", "week_sin", "week_cos"]
    X = ts[features].values
    y = ts["next_week_enrolled"].values

    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
    )
    model.fit(X, y)

    scores = cross_val_score(model, X, y, cv=5, scoring="r2")
    metrics = {
        "model_type": "GradientBoostingRegressor",
        "r2_mean": round(float(scores.mean()), 4),
        "r2_std": round(float(scores.std()), 4),
        "n_samples": len(X),
        "features": features,
        "trained_at": datetime.now().isoformat(),
    }

    with open(os.path.join(MODEL_DIR, "enrollment_forecaster.pkl"), "wb") as f:
        pickle.dump(model, f)
    with open(os.path.join(MODEL_DIR, "enrollment_forecaster_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"  Enrollment model R2: {metrics['r2_mean']:.4f} (+/- {metrics['r2_std']:.4f})")
    return model, metrics


def train_risk_classifier():
    """
    Train a model to classify site risk levels.
    Uses site operational metrics to predict risk category.
    """
    print("Training site risk classifier...")
    sites = pd.read_csv(os.path.join(DATA_DIR, "sites.csv"))

    # Create risk labels based on composite of quality indicators
    sites["risk_label"] = pd.cut(
        sites["quality_score"],
        bins=[0, 0.5, 0.7, 1.0],
        labels=["High Risk", "Medium Risk", "Low Risk"]
    )

    features = ["enrollment_rate_per_month", "screen_fail_rate",
                 "query_rate_per_100_crfs", "protocol_deviations",
                 "major_deviations", "days_to_activate",
                 "monitoring_visits_completed"]
    X = sites[features].fillna(0).values

    le = LabelEncoder()
    y = le.fit_transform(sites["risk_label"])

    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        random_state=42,
    )
    model.fit(X, y)

    scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
    feature_importance = dict(zip(features, [round(float(x), 4) for x in model.feature_importances_]))

    metrics = {
        "model_type": "RandomForestClassifier",
        "accuracy_mean": round(float(scores.mean()), 4),
        "accuracy_std": round(float(scores.std()), 4),
        "n_samples": len(X),
        "features": features,
        "feature_importance": feature_importance,
        "classes": le.classes_.tolist(),
        "trained_at": datetime.now().isoformat(),
    }

    with open(os.path.join(MODEL_DIR, "risk_classifier.pkl"), "wb") as f:
        pickle.dump({"model": model, "label_encoder": le}, f)
    with open(os.path.join(MODEL_DIR, "risk_classifier_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"  Risk classifier accuracy: {metrics['accuracy_mean']:.4f} (+/- {metrics['accuracy_std']:.4f})")
    return model, metrics


def compute_site_rankings():
    """
    Compute composite site ranking scores.
    Weighted combination of enrollment performance, quality, and compliance.
    """
    print("Computing site rankings...")
    sites = pd.read_csv(os.path.join(DATA_DIR, "sites.csv"))

    # Normalize metrics to 0-1 scale
    def min_max_scale(series):
        mn, mx = series.min(), series.max()
        if mx == mn:
            return pd.Series(0.5, index=series.index)
        return (series - mn) / (mx - mn)

    # Higher is better
    sites["enrollment_score"] = min_max_scale(sites["enrollment_rate_per_month"])
    sites["quality_norm"] = min_max_scale(sites["quality_score"])

    # Lower is better (invert)
    sites["screen_fail_score"] = 1 - min_max_scale(sites["screen_fail_rate"])
    sites["query_score"] = 1 - min_max_scale(sites["query_rate_per_100_crfs"])
    sites["deviation_score"] = 1 - min_max_scale(sites["protocol_deviations"])
    sites["activation_score"] = 1 - min_max_scale(sites["days_to_activate"])

    # Weighted composite
    weights = {
        "enrollment_score": 0.25,
        "quality_norm": 0.20,
        "screen_fail_score": 0.15,
        "query_score": 0.15,
        "deviation_score": 0.15,
        "activation_score": 0.10,
    }

    sites["composite_rank_score"] = sum(
        sites[col] * w for col, w in weights.items()
    )

    # Rank within each study
    sites["rank_within_study"] = sites.groupby("study_id")["composite_rank_score"].rank(
        ascending=False, method="min"
    ).astype(int)

    # Tier assignment
    sites["performance_tier"] = pd.cut(
        sites["composite_rank_score"],
        bins=[0, 0.35, 0.55, 0.75, 1.0],
        labels=["Underperforming", "Below Average", "Good", "Top Performer"]
    )

    ranking_cols = [
        "study_id", "site_id", "site_name", "country", "investigator",
        "enrollment_score", "quality_norm", "screen_fail_score",
        "query_score", "deviation_score", "activation_score",
        "composite_rank_score", "rank_within_study", "performance_tier",
    ]

    rankings = sites[ranking_cols].sort_values(
        ["study_id", "rank_within_study"]
    )

    rankings.to_csv(os.path.join(DATA_DIR, "site_rankings.csv"), index=False)

    summary = {
        "n_sites_ranked": len(rankings),
        "tier_distribution": rankings["performance_tier"].value_counts().to_dict(),
        "avg_composite_score": round(float(rankings["composite_rank_score"].mean()), 4),
        "weights_used": weights,
        "computed_at": datetime.now().isoformat(),
    }

    with open(os.path.join(MODEL_DIR, "site_ranking_config.json"), "w") as f:
        json.dump(summary, f, indent=2, default=str)

    print(f"  Ranked {len(rankings)} sites across {rankings['study_id'].nunique()} studies")
    return rankings, summary


def main():
    print("=" * 60)
    print("Clinical Control Tower - Model Training Pipeline")
    print("=" * 60)

    train_enrollment_forecaster()
    train_risk_classifier()
    compute_site_rankings()

    print("\nAll models trained and saved successfully.")
    print(f"Artifacts saved to: {MODEL_DIR}")


if __name__ == "__main__":
    main()
