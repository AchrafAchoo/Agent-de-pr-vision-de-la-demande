from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.loaders.m5 import load_m5
from src.features.build import build_features

HORIZON = 28

df = load_m5(states=["CA"], max_series=500)   # small subset first
df = build_features(df, horizon=HORIZON)

print(df.shape)
print(df.columns.tolist())
print(df.isna().mean().sort_values(ascending=False).head(10))

df.to_parquet("data/m5_features.parquet")