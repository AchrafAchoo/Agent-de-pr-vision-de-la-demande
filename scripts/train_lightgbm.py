import argparse
from pathlib import Path
import sys

import joblib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loaders.m5 import load_m5
from src.models.lightgbm_model import train_lightgbm


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train a LightGBM model and forecast the final 28 M5 sample days."
    )
    parser.add_argument(
        "--max-series",
        type=int,
        default=500,
        help="Number of M5 series to load (default: 500).",
    )
    parser.add_argument(
        "--model-output",
        type=Path,
        default=ROOT / "data" / "m5_lightgbm_model.joblib",
        help="Path for the trained LightGBM model.",
    )
    parser.add_argument(
        "--forecast-output",
        type=Path,
        default=ROOT / "data" / "m5_lightgbm_forecast.csv",
        help="CSV path for the 28-day forecasts.",
    )
    args = parser.parse_args()
    if args.max_series < 1:
        parser.error("--max-series must be positive.")

    data = load_m5(max_series=args.max_series, use_cache=False)
    model, forecast = train_lightgbm(data)

    args.model_output.parent.mkdir(parents=True, exist_ok=True)
    args.forecast_output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.model_output)
    forecast.to_csv(args.forecast_output, index=False)

    print(
        f"Saved {len(forecast)} forecasts for "
        f"{forecast['unique_id'].nunique()} series (28 days each)."
    )
    print(f"Model: {args.model_output}")
    print(f"Forecast: {args.forecast_output}")


if __name__ == "__main__":
    main()
