"""LightGBM forecasting for the final holdout days of each series."""

from numbers import Integral

import lightgbm as lgb
import numpy as np
import pandas as pd

from src.features.build import build_features


def train_lightgbm(
    data: pd.DataFrame, horizon: int = 28
) -> tuple[lgb.LGBMRegressor, pd.DataFrame]:
    """Train on each series' history and forecast its final ``horizon`` days."""
    if isinstance(horizon, bool) or not isinstance(horizon, Integral) or horizon < 1:
        raise ValueError("horizon must be a positive integer.")

    required = {"unique_id", "ds", "y"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}.")
    if data.empty:
        raise ValueError("At least one observation is required.")

    observations = data.copy()
    observations["ds"] = pd.to_datetime(observations["ds"], errors="raise")
    observations["y"] = pd.to_numeric(observations["y"], errors="raise")
    if observations[["unique_id", "ds", "y"]].isna().any().any():
        raise ValueError("Series IDs, dates, and targets must not be null.")
    if not np.isfinite(observations["y"].to_numpy(dtype=float)).all():
        raise ValueError("Target values must be finite.")
    if observations["y"].lt(0).any():
        raise ValueError("Poisson regression requires non-negative targets.")
    if observations.duplicated(["unique_id", "ds"]).any():
        raise ValueError("Each series must have at most one observation per date.")

    observations = observations.sort_values(["unique_id", "ds"])
    features = build_features(observations, horizon=horizon)
    grouped = features.groupby("unique_id", observed=True, sort=False)
    row_numbers = grouped.cumcount()
    series_sizes = grouped["unique_id"].transform("size")
    train_mask = row_numbers.lt(series_sizes - horizon)
    forecast_rows = features.loc[~train_mask]
    if forecast_rows.empty or train_mask.sum() == 0:
        raise ValueError("Each series needs more observations than the forecast horizon.")
    if forecast_rows.groupby("unique_id", observed=True).size().ne(horizon).any():
        raise ValueError("Each series must contain at least one full forecast horizon.")

    feature_columns = [
        column for column in features.columns if column not in {"unique_id", "ds", "y"}
    ]
    if not feature_columns:
        raise ValueError("No model features are available.")

    model = lgb.LGBMRegressor(
        objective="poisson",
        n_estimators=100,
        learning_rate=0.05,
        num_leaves=31,
        random_state=42,
        n_jobs=4,
        verbosity=-1,
    )
    model.fit(features.loc[train_mask, feature_columns], features.loc[train_mask, "y"])

    predictions = model.predict(forecast_rows[feature_columns])
    forecast = forecast_rows[["unique_id", "ds"]].copy()
    forecast["y_hat"] = np.maximum(predictions, 0)
    return model, forecast.reset_index(drop=True)
