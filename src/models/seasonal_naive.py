"""Weekly seasonal-naive forecasting and holdout evaluation."""

from numbers import Integral

import numpy as np
import pandas as pd


def _validate_period(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 1:
        raise ValueError(f"{name} must be a positive integer.")
    return int(value)


def _validate_observations(
    frame: pd.DataFrame, value_column: str
) -> pd.DataFrame:
    columns = ["unique_id", "ds", value_column]
    missing = set(columns).difference(frame.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}.")
    if frame.empty:
        raise ValueError("At least one observation is required.")

    observations = frame[columns].copy()
    if observations[["unique_id", "ds", value_column]].isna().any().any():
        raise ValueError("Series IDs, dates, and values must not be null.")
    observations["ds"] = pd.to_datetime(observations["ds"], errors="raise")
    observations[value_column] = pd.to_numeric(
        observations[value_column], errors="raise"
    )
    if not np.isfinite(observations[value_column].to_numpy(dtype=float)).all():
        raise ValueError("Observed values must be finite.")
    if observations.duplicated(["unique_id", "ds"]).any():
        raise ValueError("Each series must have at most one observation per date.")
    return observations.sort_values(["unique_id", "ds"])


def seasonal_naive_forecast(
    history: pd.DataFrame,
    horizon: int = 28,
    season_length: int = 7,
) -> pd.DataFrame:
    """Repeat each series' latest seasonal cycle for the requested horizon."""
    horizon = _validate_period(horizon, "horizon")
    season_length = _validate_period(season_length, "season_length")
    observations = _validate_observations(history, "y")

    forecasts = []
    for unique_id, series in observations.groupby(
        "unique_id", sort=False, observed=True
    ):
        if len(series) < season_length:
            raise ValueError(
                f"Series {unique_id!r} needs at least {season_length} observations."
            )

        recent = series.tail(season_length)
        if not recent["ds"].diff().iloc[1:].eq(pd.Timedelta(days=1)).all():
            raise ValueError(
                f"Series {unique_id!r} must have consecutive daily observations "
                f"for its latest {season_length} values."
            )

        dates = pd.date_range(
            start=series["ds"].iloc[-1] + pd.Timedelta(days=1),
            periods=horizon,
            freq="D",
        )
        values = np.resize(recent["y"].to_numpy(dtype=float), horizon)
        forecasts.append(
            pd.DataFrame(
                {"unique_id": unique_id, "ds": dates, "y_hat": values}
            )
        )

    return pd.concat(forecasts, ignore_index=True)


def evaluate_forecast(
    actual: pd.DataFrame, forecast: pd.DataFrame
) -> dict[str, float]:
    """Calculate pooled MAE, RMSE, and sMAPE (as a percentage)."""
    observations = _validate_observations(actual, "y")
    predictions = _validate_observations(forecast, "y_hat")
    comparison = observations.merge(
        predictions,
        on=["unique_id", "ds"],
        how="outer",
        validate="one_to_one",
        indicator=True,
    )
    if not comparison["_merge"].eq("both").all():
        raise ValueError("Actual and forecast series must have matching dates.")

    actual_values = comparison["y"].to_numpy(dtype=float)
    predicted_values = comparison["y_hat"].to_numpy(dtype=float)
    absolute_errors = np.abs(actual_values - predicted_values)
    denominators = np.abs(actual_values) + np.abs(predicted_values)
    smape_terms = np.divide(
        2 * absolute_errors,
        denominators,
        out=np.zeros_like(absolute_errors),
        where=denominators != 0,
    )
    return {
        "mae": float(absolute_errors.mean()),
        "rmse": float(np.sqrt(np.square(absolute_errors).mean())),
        "smape": float(smape_terms.mean() * 100),
    }


def backtest_seasonal_naive(
    data: pd.DataFrame,
    horizon: int = 28,
    season_length: int = 7,
) -> dict[str, float]:
    """Evaluate the model on the latest ``horizon`` days of every series."""
    horizon = _validate_period(horizon, "horizon")
    season_length = _validate_period(season_length, "season_length")
    observations = _validate_observations(data, "y")

    actuals = []
    forecasts = []
    for unique_id, series in observations.groupby(
        "unique_id", sort=False, observed=True
    ):
        if len(series) < horizon + season_length:
            raise ValueError(
                f"Series {unique_id!r} needs at least "
                f"{horizon + season_length} observations for backtesting."
            )
        train = series.iloc[:-horizon]
        actuals.append(series.iloc[-horizon:])
        forecasts.append(
            seasonal_naive_forecast(
                train, horizon=horizon, season_length=season_length
            )
        )

    return evaluate_forecast(
        pd.concat(actuals, ignore_index=True),
        pd.concat(forecasts, ignore_index=True),
    )
