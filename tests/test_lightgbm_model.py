import numpy as np
import pandas as pd
import pytest

from src.models.lightgbm_model import train_lightgbm


def make_sample(days=70):
    dates = pd.date_range("2024-01-01", periods=days, freq="D")
    frames = []
    for series, offset in (("series_a", 0), ("series_b", 3)):
        frames.append(
            pd.DataFrame(
                {
                    "unique_id": series,
                    "ds": dates,
                    "y": (np.arange(days) % 7 + offset).astype(float),
                    "sell_price": 1.0,
                    "item_id": series,
                }
            )
        )
    return pd.concat(frames, ignore_index=True)


def test_lightgbm_forecasts_the_last_28_days_for_each_series():
    model, forecast = train_lightgbm(make_sample())

    assert forecast.groupby("unique_id", observed=True).size().to_dict() == {
        "series_a": 28,
        "series_b": 28,
    }
    assert forecast.groupby("unique_id", observed=True)["ds"].min().eq(
        pd.Timestamp("2024-02-12")
    ).all()
    assert np.isfinite(forecast["y_hat"]).all()
    assert forecast["y_hat"].ge(0).all()
    assert model.n_features_in_ > 0


def test_holdout_targets_do_not_change_forecasts():
    sample = make_sample()
    _, original = train_lightgbm(sample)
    changed = sample.copy()
    holdout = changed.groupby("unique_id", observed=True).cumcount() >= len(
        changed) // changed["unique_id"].nunique() - 28
    changed.loc[holdout, "y"] += 1000
    _, updated = train_lightgbm(changed)

    pd.testing.assert_frame_equal(original, updated)


@pytest.mark.parametrize("horizon", [0, -1, 1.5, True])
def test_lightgbm_rejects_invalid_horizon(horizon):
    with pytest.raises(ValueError, match="horizon must be a positive integer"):
        train_lightgbm(make_sample(), horizon=horizon)
