import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.loaders.m5 import load_m5_frames

parser = argparse.ArgumentParser(description="Load M5 sales data.")
group = parser.add_mutually_exclusive_group()
group.add_argument(
    "--max-series",
    type=int,
    default=500,
    help="Load only the first N series to limit memory use (default: 500).",
)
group.add_argument(
    "--all",
    action="store_true",
    help="Load the complete M5 dataset; this can require several GB of RAM.",
)
args = parser.parse_args()

Y_df, X_df, S_df = load_m5_frames(
    Path(__file__).resolve().parents[1] / "data",
    max_series=None if args.all else args.max_series,
)

print(Y_df.shape, X_df.shape, S_df.shape)
print(Y_df.head())

# Save the selected dataframes for quick reload.
data_dir = Path(__file__).resolve().parents[1] / "data"
suffix = "" if args.all else f"_sample_{args.max_series}"
Y_df.to_parquet(data_dir / f"m5_sales{suffix}.parquet")
X_df.to_parquet(data_dir / f"m5_exog{suffix}.parquet")
S_df.to_parquet(data_dir / f"m5_static{suffix}.parquet")