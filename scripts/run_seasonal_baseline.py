import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.loaders.m5 import load_m5
from src.models.seasonal_naive import (
    backtest_seasonal_naive,
    seasonal_naive_forecast,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backtest and forecast with the weekly seasonal-naive baseline."
    )
    parser.add_argument(
        "--max-series",
        type=int,
        default=20,
        help="Number of M5 series to load (default: 20).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "m5_seasonal_naive_forecast.csv",
        help="CSV path for the 28-day forecasts.",
    )
    args = parser.parse_args()
    if args.max_series < 1:
        parser.error("--max-series must be positive.")

    data = load_m5(max_series=args.max_series, use_cache=False)
    metrics = backtest_seasonal_naive(data)
    forecast = seasonal_naive_forecast(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    forecast.to_csv(args.output, index=False)

    print(f"Backtest on {data['unique_id'].nunique()} series (28 days):")
    for metric, value in metrics.items():
        print(f"{metric.upper()}: {value:.4f}")
    print(f"Saved {len(forecast)} forecasts to {args.output}")


if __name__ == "__main__":
    main()
