import numpy as np
import pandas as pd
import pytest

from src.models.seasonal_naive import (
    backtest_seasonal_naive,
    evaluate_forecast,
    seasonal_naive_forecast,
)


def test_seasonal_naive_repeats_latest_week_for_each_series():
    dates = pd.date_range("2024-01-01", periods=14, freq="D")
    history = pd.concat(
        [
            pd.DataFrame(
                {"unique_id": "series_a", "ds": dates, "y": np.arange(1, 15)}
            ),
            pd.DataFrame(
                {"unique_id": "series_b", "ds": dates, "y": np.zeros(14)}
            ),
        ],
        ignore_index=True,
    ).sample(frac=1, random_state=4)

    forecast = seasonal_naive_forecast(history)

    assert forecast.groupby("unique_id", observed=True).size().to_dict() == {
        "series_a": 28,
        "series_b": 28,
    }
    assert forecast["ds"].min() == dates[-1] + pd.Timedelta(days=1)
    assert forecast.loc[forecast["unique_id"] == "series_a", "y_hat"].tolist() == [
        8,
        9,
        10,
        11,
        12,
        13,
        14,
    ] * 4
    assert forecast.loc[forecast["unique_id"] == "series_b", "y_hat"].eq(0).all()


def test_backtest_excludes_last_28_days_from_training():
    dates = pd.date_range("2024-01-01", periods=56, freq="D")
    values = np.tile(np.arange(1, 8), 8)
    data = pd.DataFrame({"unique_id": "series_a", "ds": dates, "y": values})

    metrics = backtest_seasonal_naive(data)

    assert metrics == {"mae": 0.0, "rmse": 0.0, "smape": 0.0}


def test_evaluate_forecast_handles_days_when_actual_and_prediction_are_zero():
    dates = pd.date_range("2024-01-01", periods=2, freq="D")
    actual = pd.DataFrame({"unique_id": "series_a", "ds": dates, "y": [0, 2]})
    forecast = pd.DataFrame(
        {"unique_id": "series_a", "ds": dates, "y_hat": [0, 1]}
    )

    metrics = evaluate_forecast(actual, forecast)

    assert metrics["mae"] == 0.5
    assert metrics["rmse"] == pytest.approx(np.sqrt(0.5))
    assert metrics["smape"] == pytest.approx(100 / 3)


def test_forecast_rejects_series_without_a_complete_season():
    history = pd.DataFrame(
        {
            "unique_id": ["series_a"] * 6,
            "ds": pd.date_range("2024-01-01", periods=6, freq="D"),
            "y": range(6),
        }
    )

    with pytest.raises(ValueError, match="at least 7 observations"):
        seasonal_naive_forecast(history)
