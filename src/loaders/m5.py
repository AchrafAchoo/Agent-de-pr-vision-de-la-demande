from pathlib import Path
import pandas as pd

DATA_DIR = Path("../../data")


def load_m5(states=None, stores=None, max_series=None, use_cache=True) -> pd.DataFrame:
    """Return M5 in the common format: unique_id, ds, y + exogenous + static columns."""
    if use_cache and (DATA_DIR / "m5_sales.parquet").exists():
        Y = pd.read_parquet(DATA_DIR / "m5_sales.parquet")
        X = pd.read_parquet(DATA_DIR / "m5_exog.parquet")
        S = pd.read_parquet(DATA_DIR / "m5_static.parquet")
    else:
        from datasetsforecast.m5 import M5
        Y, X, S = M5.load(str(DATA_DIR))

    # --- subset (applied early to save RAM) ---
    if states:
        S = S[S["state_id"].isin(states)]
    if stores:
        S = S[S["store_id"].isin(stores)]
    if max_series:
        S = S.head(max_series)
    ids = S["unique_id"].unique()
    Y = Y[Y["unique_id"].isin(ids)]
    X = X[X["unique_id"].isin(ids)]

    # --- merge into one dataframe ---
    df = Y.merge(X, on=["unique_id", "ds"], how="left")
    df = df.merge(S, on="unique_id", how="left")
    df["ds"] = pd.to_datetime(df["ds"])

    # --- promo proxy: price below 95% of the item's average price ---
    if "sell_price" in df.columns:
        avg_price = df.groupby("unique_id")["sell_price"].transform("mean")
        df["promo"] = (df["sell_price"] / avg_price < 0.95).astype(int)

    return df.sort_values(["unique_id", "ds"]).reset_index(drop=True)


if __name__ == "__main__":
    df = load_m5(states=["CA"], max_series=500)
    print(df.shape)
    print(df.columns.tolist())
    print(df.head())